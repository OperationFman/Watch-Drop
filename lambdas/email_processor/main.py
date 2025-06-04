import os
import boto3   # type: ignore
import json
import re
from botocore.exceptions import ClientError # type: ignore

dynamodb_client = boto3.client('dynamodb')

DYNAMODB_TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME')

if not DYNAMODB_TABLE_NAME:
    raise ValueError("DYNAMODB_TABLE_NAME environment variable not set for Email Processor Lambda.")

TMDB_URL_REGEX = re.compile(r'themoviedb\.org/(movie|tv)/([a-zA-Z0-9\-]+)')

def lambda_handler(event, context):
    print(f"Email Processor Lambda triggered by event: {json.dumps(event)}")

    for record in event['Records']:
        if 'ses' not in record:
            print("Record is not an SES email receiving event. Skipping.")
            continue

        mail_data = record['ses']['mail']
        sender_email = mail_data['commonHeaders']['from'][0]
        subject = mail_data['commonHeaders']['subject']

        print(f"Processing email from '{sender_email}' with subject: '{subject}'")

        command_type = None
        tmdb_full_id = None
        tmdb_content_type = None

        subject_lower = subject.lower().strip()

        if subject_lower.startswith("add "):
            command_type = "add"
        elif subject_lower.startswith("remove "):
            command_type = "remove"
        
        if command_type:
            url_part = subject_lower[len(command_type) + 1:].strip()
            
            match = TMDB_URL_REGEX.search(url_part)
            if match:
                tmdb_content_type = match.group(1)
                tmdb_full_id = match.group(2)
            else:
                print(f"  Could not extract valid TMDB URL from subject: '{subject}'. Skipping.")
                continue

        if not command_type or not tmdb_full_id:
            print(f"  No valid 'add' or 'remove' command or TMDB ID found in subject: '{subject}'. Skipping.")
            continue

        print(f"  Detected command: '{command_type}', TMDB ID: '{tmdb_full_id}', Type: '{tmdb_content_type}' for user: '{sender_email}'")

        try:
            if command_type == "add":
                dynamodb_client.put_item(
                    TableName=DYNAMODB_TABLE_NAME,
                    Item={
                        'user_email': {'S': sender_email},
                        'tmdb_id': {'S': tmdb_full_id},
                        'tmdb_type': {'S': tmdb_content_type}
                    }
                )
                print(f"  Successfully added/updated subscription for '{sender_email}' to TMDB ID '{tmdb_full_id}'.")
                # TODO: confirmation email via ses_sender

            elif command_type == "remove":
                dynamodb_client.delete_item(
                    TableName=DYNAMODB_TABLE_NAME,
                    Key={
                        'user_email': {'S': sender_email},
                        'tmdb_id': {'S': tmdb_full_id}
                    }
                )
                print(f"  Successfully removed subscription for '{sender_email}' from TMDB ID '{tmdb_full_id}'.")
                # TODO: confirmation email via ses_sender

        except ClientError as e:
            print(f"  DynamoDB operation failed for '{command_type}' command for '{sender_email}': {e}")
            # TODO: confirmation email via ses_sender
        except Exception as e:
            print(f"  An unexpected error occurred during DynamoDB operation for '{sender_email}': {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Email processing complete.')
    }