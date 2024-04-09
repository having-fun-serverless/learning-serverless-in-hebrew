import boto3
import json
import os
import re
from boto3.dynamodb.conditions import Key
from datetime import datetime
import random
import string
import base64

s3 = boto3.resource("s3")
bucket = s3.Bucket(os.environ["MESSAGES_BUCKET"])

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])

secret_manager = boto3.client("secretsmanager")
secret_id = os.environ["SECRET_ID"]
USER = os.environ["USER"]

def lambda_handler(event, context):
    if not is_valid_token(event["headers"]["Authorization"]):
        return {
            "statusCode": 401, 
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "GET",
            }
        }
    
    
        
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
    return {
        "statusCode": 200, 
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*", 
            "Access-Control-Allow-Methods": "POST",
        }
    }


def is_valid_token(token: str):
     if token and token.startswith("Basic"):
        decoded_auth = base64.b64decode(token[6:]).decode()
        username, password = decoded_auth.split(":")
        secret = secret_manager.get_secret_value(SecretId=secret_id)["SecretString"]
        return username == USER and password == secret