import boto3

def lambda_handler(event, context):
    client = boto3.client('lambda')
    response = client.invoke(FunctionName="function2-iam")
    return response["Payload"].read().decode("utf-8")
