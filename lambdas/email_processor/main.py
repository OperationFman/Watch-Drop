import os
import boto3 #type: ignore
import json
import re
from botocore.exceptions import ClientError #type: ignore

dynamodb_client = boto3.client('dynamodb')

EMAIL_PARSE_REGEX = re.compile(r'<([^>]+)>|([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
TMDB_URL_REGEX = re.compile(r'themoviedb\.org/(movie|tv)/([a-zA-Z0-9\-]+)')

def extract_email_address(full_from_string):
    match = EMAIL_PARSE_REGEX.search(full_from_string)
    if match: return match.group(1) or match.group(2)
    return full_from_string

def lambda_handler(event, context):
    table_name = os.environ.get('DYNAMODB_TABLE_NAME')
    if not table_name: raise ValueError("DYNAMODB_TABLE_NAME not set.")

    for record in event['Records']:
        if 'ses' not in record: continue

        sender_email = extract_email_address(record['ses']['mail']['commonHeaders']['from'][0])
        subject_lower = record['ses']['mail']['commonHeaders']['subject'].lower().strip()

        try:
            if subject_lower == "nuke account":
                response = dynamodb_client.query(TableName=table_name, KeyConditionExpression='user_email = :e', ExpressionAttributeValues={':e': {'S': sender_email}})
                for item in response.get('Items', []):
                    dynamodb_client.delete_item(TableName=table_name, Key={'user_email': {'S': sender_email}, 'tmdb_id': {'S': item['tmdb_id']['S']}})
                continue

            command_prefix = None
            if subject_lower.startswith("add "): command_prefix = "add"
            elif subject_lower.startswith("remove "): command_prefix = "remove"
            
            if not command_prefix: continue
            
            url_part = subject_lower[len(command_prefix) + 1:].strip()
            match = TMDB_URL_REGEX.search(url_part)
            
            if not match: continue
            
            content_type, tmdb_id = match.groups()
            if content_type != 'tv': continue

            if command_prefix == "add":
                dynamodb_client.put_item(TableName=table_name, Item={'user_email': {'S': sender_email.lower()}, 'tmdb_id': {'S': tmdb_id}})
            else:
                dynamodb_client.delete_item(TableName=table_name, Key={'user_email': {'S': sender_email.lower()}, 'tmdb_id': {'S': tmdb_id}})
            
        except ClientError as e:
            print(f"DynamoDB operation failed for command '{command_prefix or subject_lower}' for '{sender_email}': {e}")

    return {'statusCode': 200, 'body': json.dumps('Email processing complete.')}
