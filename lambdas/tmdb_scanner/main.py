import os
import boto3 # type: ignore
import json
from botocore.exceptions import ClientError # type: ignore
import requests # type: ignore
from datetime import datetime, timedelta
import re

secretsmanager_client = boto3.client('secretsmanager')
dynamodb_client = boto3.client('dynamodb')

TMDB_API_SECRET_NAME = os.environ.get('TMDB_API_SECRET_NAME')
DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')

if not TMDB_API_SECRET_NAME:
    raise ValueError("TMDB_API_SECRET_NAME environment variable not set.")
if not DYNAMODB_TABLE_NAME:
    raise ValueError("DYNAMODB_TABLE_NAME environment variable not set.")

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
        tmdb_id = item['tmdb_id']['S']

        tmdb_type = item.get('tmdb_type', {}).get('S', 'tv') 

        api_url = ""
        if tmdb_type == 'tv':
            api_url = f"{TMDB_BASE_URL}/tv/{tmdb_id}?language=en-US"
        elif tmdb_type == 'movie':
            api_url = f"{TMDB_BASE_URL}/movie/{tmdb_id}?language=en-US"
        else:
            print(f"Skipping unknown TMDB type '{tmdb_type}' for user {user_email} and ID {tmdb_id}. Ensure tmdb_type is 'tv' or 'movie'.")
            continue

        print(f"Checking {tmdb_type} ID {tmdb_id} for user {user_email} at {api_url}")

        headers = {
            "Authorization": f"Bearer {TMDB_API_KEY}",
            "accept": "application/json"
        }

        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            tmdb_data = response.json()

            episode_aired_yesterday = False
            tmdb_air_date = None

            if tmdb_type == 'tv':
                last_episode = tmdb_data.get('last_episode_to_air')
                if last_episode and last_episode.get('air_date'):
                    tmdb_air_date = last_episode['air_date']
            elif tmdb_type == 'movie':
                tmdb_air_date = tmdb_data.get('release_date')

            if tmdb_air_date:
                episode_aired_yesterday = (tmdb_air_date == yesterday_date_str)
                print(f"  {user_email}: TMDB ID {tmdb_id} (Type: {tmdb_type}, Latest Air Date: {tmdb_air_date}) -> Aired Yesterday: {episode_aired_yesterday}")
            else:
                print(f"  {user_email}: TMDB ID {tmdb_id} (Type: {tmdb_type}) -> No valid air date found from TMDB API response.")

            if episode_aired_yesterday:
                # Placeholder Sender
                print(f"    ACTION: Detected new content for {user_email}, TMDB ID {tmdb_id}. (Aired Yesterday)")

        except requests.exceptions.RequestException as e:
            print(f"Error calling TMDB API for {tmdb_type} ID {tmdb_id}: {e}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON response from TMDB for {tmdb_type} ID {tmdb_id}.")
        except Exception as e:
            print(f"An unexpected error occurred processing {tmdb_type} ID {tmdb_id}: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('TMDB Scanner Lambda execution finished.')
    }