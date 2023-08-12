
import json

def lambda_handler(event, context):
    for record in event['Records']:
        message_body = json.loads(record['body'])
        s3_event = message_body['Records'][0]['s3']

        bucket_name = s3_event['bucket']['name']
        object_key = s3_event['object']['key']

        print(f"Bucket Name: {bucket_name}")
        print(f"Object Key: {object_key}")