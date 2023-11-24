
import json
import boto3
from boto3.dynamodb.conditions import Key
import os


s3 = boto3.client("s3")

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])

ses = boto3.client("ses")
verified_email = os.environ["VERIFIED_EMAIL"]

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])
        s3_event = message_body['Records'][0]['s3']

        bucket_name = s3_event['bucket']['name']
        object_key = s3_event['object']['key']

        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read()
        
        message = json.loads(file_content.decode('utf-8'))
        
        send_emails(group_id=message["group_id"], content=message["post"])
        
def send_emails(group_id:str, content:str):
    group_pk = f"GROUP#{group_id}"
    users_sk = "USER#"
    
    users_reponse = table.query(KeyConditionExpression=(Key('PK').eq(group_pk) & Key('SK').begins_with(users_sk)))
    key={
        'PK': group_pk,
        'SK': "METADATA#"
    }
    group_meta = table.get_item(Key=key)
    users = users_reponse["Items"]
    print(f"Found {len(users)} users")
    for user in users:
        recipient_email = user["SK"].split("#")[1]
        email_message = {
            'Subject': {'Data': f"A new message from {group_meta['Item']['name']}"},
            'Body': {
                'Html': {'Data': content},
            }
        }
        try:
            response = ses.send_email(
                Source=verified_email,
                Destination={
                    'ToAddresses': [recipient_email],
                },
                Message=email_message
            )
        
            print("Email sent successfully! Message ID: ", response['MessageId'])
        
        except Exception as e:
            print(f"Error sending email: {e}")
        