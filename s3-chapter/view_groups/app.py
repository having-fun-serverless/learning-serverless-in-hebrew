import boto3
from boto3.dynamodb.conditions import Attr
import json
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["GROUPS_SUBSCRIBERS_TABLE_NAME"])


def lambda_handler(event, context):
    response = table.scan(FilterExpression=Attr('SK').eq('METADATA#'))
    
    items = response["Items"]
    groups = []
    for item in items:
        group = {
            "id": item["PK"],
            "name": item["name"],
            "description": item["description"]
        }
        groups.append(group)
            

    return {
        "statusCode": 200,
        "body": json.dumps(groups)
    }