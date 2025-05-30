import os
import boto3 # type: ignore
import json
import base64

secretsmanager_client = boto3.client('secretsmanager')

TMDB_API_SECRET_NAME = os.environ.get('TMDB_API_SECRET_NAME')
if not TMDB_API_SECRET_NAME:
    raise ValueError("Scanner could not fetch TMDB_API_SECRET_NAME environment variable from Secrets Manager")

def get_secret(secret_name):
    try:
        get_secret_value_response = secretsmanager_client.get_secret_value(SecretId=secret_name)
    except ClientError as e: # type: ignore
        print(f"Error retrieving secret '{secret_name}': {e}")
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            return get_secret_value_response['SecretString']
        else:
            return base64.b64decode(get_secret_value_response['SecretBinary'])

TMDB_API_KEY = get_secret(TMDB_API_SECRET_NAME)

def lambda_handler(event, context):
    print(f"Using TMDB API Key (first 5 chars): {TMDB_API_KEY[:5]}*****")
    return {
        'statusCode': 200,
        'body': json.dumps('Lambda executed successfully')
    }