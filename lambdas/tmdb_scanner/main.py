import os
import boto3 # type: ignore
import json
from botocore.exceptions import ClientError # type: ignore
import requests # type: ignore
from datetime import datetime, timedelta

secretsmanager_client = boto3.client('secretsmanager')
dynamodb_client = boto3.client('dynamodb')
lambda_client = boto3.client('lambda')

TMDB_API_SECRET_NAME = os.environ.get('TMDB_API_SECRET_NAME')
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')
SES_SENDER_LAMBDA_NAME = os.environ.get('SES_SENDER_LAMBDA_NAME')

if not TMDB_API_SECRET_NAME:
    raise ValueError("TMDB_API_SECRET_NAME environment variable not set.")
if not DYNAMODB_TABLE_NAME:
    raise ValueError("DYNAMODB_TABLE_NAME environment variable not set.")
if not SES_SENDER_LAMBDA_NAME:
    raise ValueError("SES_SENDER_LAMBDA_NAME environment variable not set.")

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_secret(secret_name):
    try:
        get_secret_value_response = secretsmanager_client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        print(f"Error retrieving secret '{secret_name}': {e}")
        raise e
    else:
        return get_secret_value_response['SecretString']

TMDB_API_KEY = get_secret(TMDB_API_SECRET_NAME)

def invoke_ses_sender_lambda(recipient_email, subject, body_html, body_text):
    payload = {
        "recipient_email": recipient_email,
        "subject": subject,
        "body_html": body_html,
        "body_text": body_text
    }
    
    try:
        response = lambda_client.invoke(
            FunctionName=SES_SENDER_LAMBDA_NAME,
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        print(f"Successfully invoked SES Sender Lambda for {recipient_email}. Status code: {response['StatusCode']}")
    except ClientError as e:
        print(f"Error invoking SES Sender Lambda for {recipient_email}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during SES Sender Lambda invocation: {e}")

def lambda_handler(event, context):
    print(f"Using TMDB API Key (first 5 chars): {TMDB_API_KEY[:5]}*****")
    
    today_utc = datetime.utcnow().date()
    yesterday_utc = today_utc - timedelta(days=1)
    yesterday_date_str = yesterday_utc.strftime('%Y-%m-%d')
    print(f"Scanning for episodes/movies aired on: {yesterday_date_str} UTC")

    subscriptions = []
    last_evaluated_key = None

    while True:
        scan_args = {
            'TableName': DYNAMODB_TABLE_NAME
        }
        if last_evaluated_key: 
            scan_args['ExclusiveStartKey'] = last_evaluated_key

        try:
            response = dynamodb_client.scan(**scan_args)
            subscriptions.extend(response.get('Items', []))
            last_evaluated_key = response.get('LastEvaluatedKey')
            if not last_evaluated_key:
                break
        except ClientError as e:
            print(f"Error scanning DynamoDB table {DYNAMODB_TABLE_NAME}: {e}")
            return {
                'statusCode': 500,
                'body': json.dumps(f"Error scanning DynamoDB: {e.response['Error']['Message']}")
            }

    print(f"Found {len(subscriptions)} subscriptions in DynamoDB.")

    for item in subscriptions:
        user_email = item['user_email']['S']
        tmdb_full_slug = item['tmdb_id']['S']
        tmdb_type = item.get('tmdb_type', {}).get('S', 'tv')

        try:
            tmdb_numeric_id = tmdb_full_slug.split('-')[0]
            if not tmdb_numeric_id.isdigit():
                raise ValueError(f"Extracted numeric ID '{tmdb_numeric_id}' is not valid.")
        except Exception as e:
            print(f"Skipping subscription for user {user_email} due to malformed TMDB ID slug '{tmdb_full_slug}': {e}")
            continue

        api_url = ""
        if tmdb_type == 'tv':
            api_url = f"{TMDB_BASE_URL}/tv/{tmdb_numeric_id}?language=en-US"
        elif tmdb_type == 'movie':
            api_url = f"{TMDB_BASE_URL}/movie/{tmdb_numeric_id}?language=en-US"
        else:
            print(f"Skipping unknown TMDB type '{tmdb_type}' for user {user_email} and ID {tmdb_full_slug}. Ensure tmdb_type is 'tv' or 'movie'.")
            continue

        print(f"Checking {tmdb_type} ID {tmdb_numeric_id} (slug: {tmdb_full_slug}) for user {user_email} at {api_url}")

        headers = {
            "Authorization": f"Bearer {TMDB_API_KEY}",
            "accept": "application/json"
        }

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            tmdb_data = response.json()

            aired_recently = False
            air_date_to_check = None
            content_title = "Unknown Content"

            if tmdb_type == 'tv':
                last_episode = tmdb_data.get('last_episode_to_air')
                next_episode = tmdb_data.get('next_episode_to_air')

                if next_episode and next_episode.get('air_date'):
                    next_air_date_str = next_episode['air_date']
                    next_air_datetime = datetime.strptime(next_air_date_str, '%Y-%m-%d').date()
                    
                    if next_air_datetime == today_utc:
                        air_date_to_check = next_air_date_str
                        content_title = f"{tmdb_data.get('name', 'Unknown TV Show')} S{next_episode.get('season_number', 'N/A')}E{next_episode.get('episode_number', 'N/A')}: {next_episode.get('name', 'N/A')}"
                        aired_recently = True
                        print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}, Next Air Date: {next_air_date_str}) -> Airs Today.")
                    else:
                        print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}, Next Air Date: {next_air_date_str}) -> Upcoming Episode.")

                if not aired_recently and last_episode and last_episode.get('air_date'):
                    last_air_date_str = last_episode['air_date']
                    last_air_datetime = datetime.strptime(last_air_date_str, '%Y-%m-%d').date()
                    
                    if last_air_datetime == yesterday_utc:
                        aired_recently = True
                        air_date_to_check = last_air_date_str
                        content_title = f"{tmdb_data.get('name', 'Unknown TV Show')} S{last_episode.get('season_number', 'N/A')}E{last_episode.get('episode_number', 'N/A')}: {last_episode.get('name', 'N/A')}"
                        print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}, Last Air Date: {last_air_date_str}) -> Aired Yesterday.")
                    else:
                        print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}, Last Air Date: {last_air_date_str}) -> Not Aired Yesterday.")
                
                if not air_date_to_check and not aired_recently:
                    print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}) -> No recent or upcoming air date found in TMDB data.")

            elif tmdb_type == 'movie':
                release_date_str = tmdb_data.get('release_date')
                content_title = tmdb_data.get('title', 'Unknown Movie')

                if release_date_str:
                    release_datetime = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                    if release_datetime == yesterday_utc:
                        aired_recently = True
                        air_date_to_check = release_date_str
                        print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}, Release Date: {release_date_str}) -> Released Yesterday.")
                    elif release_datetime == today_utc:
                        aired_recently = True
                        air_date_to_check = release_date_str
                        print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}, Release Date: {release_date_str}) -> Released Today.")
                    else:
                        print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}, Release Date: {release_date_str}) -> Not Released Yesterday or Today.")
                else:
                    print(f"  {user_email}: TMDB ID {tmdb_full_slug} (Type: {tmdb_type}) -> No valid movie release date found from TMDB API response.")

            if aired_recently:
                subject = f"Watch Drop: New Content Aired! - {content_title}"
                tmdb_link = f"https://www.themoviedb.org/{tmdb_type}/{tmdb_full_slug}" 
                
                body_text = f"""
                    Hello there

                    A new {tmdb_type} you're tracking aired recently:

                    Title: {content_title}
                    Aired Date: {air_date_to_check}
                    View on TMDB: {tmdb_link}

                    Enjoy your Watch Drop!
                    """
                body_html = f"""
                <html>
                <body>
                    <h1>Hello there</h1>
                    <p>A new {tmdb_type} you're tracking just aired recently:</p>
                    <h2>✨ {content_title} ✨</h2>
                    <ul>
                        <li><strong>Aired Date:</strong> {air_date_to_check}</li>
                        <li><strong>TMDB Page:</strong> <a href="{tmdb_link}">{tmdb_link}</a></li>
                    </ul>
                    <p>Enjoy your Watch Drop!</p>
                    <p>The Watch Drop Team</p>
                </body>
                </html>
                """
                
                invoke_ses_sender_lambda(user_email, subject, body_html, body_text)
                print(f"    ACTION: Invoked SES Sender for {user_email}, TMDB ID {tmdb_full_slug}. (Aired Recently)")

        except requests.exceptions.RequestException as e:
            print(f"Error calling TMDB API for {tmdb_type} ID {tmdb_numeric_id} (slug: {tmdb_full_slug}): {e}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON response from TMDB for {tmdb_type} ID {tmdb_numeric_id} (slug: {tmdb_full_slug}).")
        except Exception as e:
            print(f"An unexpected error occurred processing {tmdb_type} ID {tmdb_numeric_id} (slug: {tmdb_full_slug}): {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('TMDB Scanner Lambda execution finished.')
    }