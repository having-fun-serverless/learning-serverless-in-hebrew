import boto3
import json
import os
import re

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])

def lambda_handler(event, context):
    group_details = json.loads(event["body"])
    # Only alphabetic characters and space are allowed
    if not re.match('^[a-zA-Z\s]+$', group_details["name"]):
        body = {"description":"Only alphabetic characters and space are allowed"}
        return {"statusCode": 500, "body": json.dumps(body)}
    group_name = group_details["name"]
    group_id = re.sub(r'\s+', '-', group_name) 
    group_description = group_details["description"]
    
    item = {"PK":f"GROUP#{group_id}", "SK":f"METADATA#", "description": group_description, "name": group_name}
    table.put_item(Item=item)
    
    return {"statusCode": 200, "body": json.dumps(item)}
         