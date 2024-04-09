import boto3
import json
import os
import re
from boto3.dynamodb.conditions import Key
from datetime import datetime
import random
import string

s3 = boto3.resource("s3")
bucket = s3.Bucket(os.environ["MESSAGES_BUCKET"])

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])


def lambda_handler(event, context):
    group_id = event["pathParameters"]["group-id"]
    message_details = json.loads(event["body"])
    # Check that group exists
    group_pk = f"GROUP#{group_id}"
    group_sk = "METADATA#"
    response = table.query(KeyConditionExpression=(Key('PK').eq(group_pk) & Key('SK').begins_with(group_sk)))
    if len(response["Items"]) == 0:
        # Group does not exist
        err_message = f"Group {group_id} not found"
        return {"statusCode": 404, "body": json.dumps({"error": err_message})}
    
    now = datetime.now()
    date_folder = now.strftime("%Y/%m/%d")
    message_details["group_id"] = group_id
    random_suffix = ''.join(random.choices(string.ascii_uppercase, k=10))
    
    object_key = f"{group_id}/{date_folder}/{random_suffix}.json"
    body = json.dumps(message_details).encode()
    bucket.put_object(Key=object_key, Body=body)
    return {"statusCode": 200}
