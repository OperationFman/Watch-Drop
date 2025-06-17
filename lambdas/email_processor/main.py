import os
import boto3 #type: ignore
import json
import re
from botocore.exceptions import ClientError #type: ignore
from responses import (
    get_nuke_confirmation_content, get_command_not_understood_content,
    get_invalid_tmdb_url_content, get_unsupported_content_type_content,
    get_add_success_content, get_remove_success_content, get_operation_failed_content,
    get_help_instructions_content
) 

dynamodb_client = boto3.client('dynamodb')
lambda_client = boto3.client('lambda')

EMAIL_PARSE_REGEX = re.compile(r'<([^>]+)>|([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
TMDB_URL_REGEX = re.compile(r'themoviedb\.org/(movie|tv)/([a-zA-Z0-9\-]+)')

def extract_email_address(full_from_string):
    match = EMAIL_PARSE_REGEX.search(full_from_string)
    if match: return match.group(1) or match.group(2)
    return full_from_string

def invoke_ses_sender_lambda(recipient_email, subject, body_html, body_text):
    ses_sender_lambda_name = os.environ.get('SES_SENDER_LAMBDA_NAME')
    payload = json.dumps({"recipient_email": recipient_email, "subject": subject, "body_html": body_html, "body_text": body_text})
    lambda_client.invoke(FunctionName=ses_sender_lambda_name, InvocationType='Event', Payload=payload)

def lambda_handler(event, context):
    table_name = os.environ.get('DYNAMODB_TABLE_NAME')

    for record in event['Records']:
        if 'ses' not in record: continue

        sender_email = extract_email_address(record['ses']['mail']['commonHeaders']['from'][0])
        subject_lower = record['ses']['mail']['commonHeaders']['subject'].lower().strip()

        subject, body_html, body_text = "", "", ""

        try:
            if subject_lower == "nuke account":
                response = dynamodb_client.query(TableName=table_name, KeyConditionExpression='user_email = :e', ExpressionAttributeValues={':e': {'S': sender_email.lower()}})
                items_nuked = len(response.get('Items', []))
                for item in response.get('Items', []):
                    dynamodb_client.delete_item(TableName=table_name, Key={'user_email': {'S': sender_email.lower()}, 'tmdb_id': {'S': item['tmdb_id']['S']}})
                subject, body_html, body_text = get_nuke_confirmation_content(items_nuked)
                invoke_ses_sender_lambda(sender_email, subject, body_html, body_text)
                continue
            
            if subject_lower == "help":
                subject, body_html, body_text = get_help_instructions_content()
                invoke_ses_sender_lambda(sender_email, subject, body_html, body_text)
                continue

            command_prefix = None
            if subject_lower.startswith("add "): command_prefix = "add"
            elif subject_lower.startswith("remove "): command_prefix = "remove"
            
            if not command_prefix:
                subject, body_html, body_text = get_command_not_understood_content(subject_lower)
                invoke_ses_sender_lambda(sender_email, subject, body_html, body_text)
                continue
            
            url_part = subject_lower[len(command_prefix) + 1:].strip()
            match = TMDB_URL_REGEX.search(url_part)
            
            if not match:
                subject, body_html, body_text = get_invalid_tmdb_url_content(url_part)
                invoke_ses_sender_lambda(sender_email, subject, body_html, body_text)
                continue
            
            content_type, tmdb_id = match.groups()
            if content_type != 'tv':
                subject, body_html, body_text = get_unsupported_content_type_content(content_type)
                invoke_ses_sender_lambda(sender_email, subject, body_html, body_text)
                continue

            if command_prefix == "add":
                dynamodb_client.put_item(TableName=table_name, Item={'user_email': {'S': sender_email.lower()}, 'tmdb_id': {'S': tmdb_id}})
                subject, body_html, body_text = get_add_success_content(tmdb_id)
                invoke_ses_sender_lambda(sender_email, subject, body_html, body_text)
            else:
                dynamodb_client.delete_item(TableName=table_name, Key={'user_email': {'S': sender_email.lower()}, 'tmdb_id': {'S': tmdb_id}})
                subject, body_html, body_text = get_remove_success_content(tmdb_id)
                invoke_ses_sender_lambda(sender_email, subject, body_html, body_text)
            
        except ClientError as e:
            subject, body_html, body_text = get_operation_failed_content(command_prefix or subject_lower, str(e))
            invoke_ses_sender_lambda(sender_email, subject, body_html, body_text)

    return {'statusCode': 200, 'body': json.dumps('Email processing complete.')}