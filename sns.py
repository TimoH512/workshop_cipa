import boto3

def sns():
    client = boto3.client('s3')
    sns = boto3.resource('sns')
    sns.