import boto3
import os
import base64

secret_manager = boto3.client("secretsmanager")
secret_id = os.environ["SECRET_ID"]
USER = os.environ["USER"]

def lambda_handler(event, context):
    status_code = 401
    if is_valid_token(event["headers"]["Authorization"]):
        status_code = 200
    
    return {
            "statusCode": status_code, 
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*", 
                "Access-Control-Allow-Methods": "GET",
            }
        }
    
def is_valid_token(token: str) -> bool:
     if token and token.startswith("Basic"):
        decoded_auth = base64.b64decode(token[6:]).decode()
        username, password = decoded_auth.split(":")
        secret = secret_manager.get_secret_value(SecretId=secret_id)["SecretString"]
        return username == USER and password == secret
