import boto3
import json
import os
import re

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])

def lambda_handler(event, context):
    group_details = json.loads(event["body"])
    # Only alpha numeric characters and space are allowed
    if not re.match('[a-zA-Z\s]+$', group_details["name"]):
        return {"statusCode": 500, "body": json.dumps({"description":"Only alpha numeric characters and space are allowed"})}
    group_name = group_details["name"]
    group_id = group_name.replace(" ", "-")
    group_description = group_details["description"]
    
    item = {"PK":"GROUP", "SK":f"GROUP#METADATA#{group_id}", "description": group_description, "name": group_name}
    table.put_item(Item=item)
    
    return {"statusCode": 200, "body": json.dumps(item)}
         
    
  
    
