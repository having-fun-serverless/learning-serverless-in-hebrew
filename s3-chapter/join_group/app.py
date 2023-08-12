import boto3
import json
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])

def lambda_handler(event, context):
    group_id = event["pathParameters"]["group-id"]
    user_details = json.loads(event["body"])
    user_email = user_details["email"]
    user_item = {"PK": f"USER#{user_email}", "SK":group_id}
    group_item = {"PK": f"GROUP#{group_id}", "SK":f"USER#{user_email}"} 
    table.put_item(Item=user_item)
    table.put_item(Item=group_item)
    return {"statusCode": 200, "body": json.dumps({"user": user_item, "group": group_item})}
