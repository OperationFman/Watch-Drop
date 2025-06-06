import os
import boto3  # type: ignore
import json
from botocore.exceptions import ClientError # type: ignore

ses_client = boto3.client('ses')
SES_SENDER_EMAIL = os.environ.get('SES_SENDER_EMAIL')

def send_notification_email(recipient_email, subject, body_html, body_text):
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient_email,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject,
                },
            },
            Source=SES_SENDER_EMAIL,
        )
        print(f"Email sent successfully to {recipient_email}! Message ID: {response['MessageId']}")
        return response['MessageId']
    except ClientError as e:
        print(f"Failed to send email to {recipient_email}. Error: {e.response['Error']['Code']} - {e.response['Error']['Message']}")
        raise e 

def lambda_handler(event, context):
    print(f"SES Sender Lambda triggered for event: {json.dumps(event)}")

    recipient_email = event.get('recipient_email')
    subject = event.get('subject')
    body_html = event.get('body_html')
    body_text = event.get('body_text')

    if not all([recipient_email, subject, body_html, body_text]):
        print("Missing required email parameters in event payload.")
        return {
            'statusCode': 400,
            'body': json.dumps("Missing email parameters.")
        }

    try:
        message_id = send_notification_email(recipient_email, subject, body_html, body_text)
        return {
            'statusCode': 200,
            'body': json.dumps(f"Email sent successfully! Message ID: {message_id}")
        }
    except Exception as e:
        print(f"Chad error in SES Sender Lambda: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Failed to send email: {str(e)}")
        }