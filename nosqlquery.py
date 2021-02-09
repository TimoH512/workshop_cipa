import json
import boto3
import os
import decimal

from boto3.dynamodb.conditions import Key, Attr


def getKey(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    key = event['pathParameters']['key']

    result = table.query(KeyConditionExpression=Key('timestamp').eq(key))

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }
    return response


def getField(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    scan_kwargs = {
        'FilterExpression': Key('nr1').eq(1),
        'FilterExpression': Key('nr2').eq(555),
    }

    result = table.scan(**scan_kwargs)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }
    return response


def getLatest(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    scan_kwargs = {
        "TableName": "workshop-cipa-dev-calcAcess-SU2DRSZND93C",
        "IndexName": "calcAcess_Index1",
        "KeyConditions": {
            "statuscode": {
                "ComparisonOperator": "EQ",
                "AttributeValueList": [
                    "200"
                ]
            }
        },
        "ScanIndexForward": False
    }

    result = table.query(**scan_kwargs)

    # create a response -> Nur den Ersten ausgeben [0]
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'][0], cls=DecimalEncoder)
    }
    return response


# Rückgabe von DynamoDB umwandeln damit JSON die Daten verarbeiten kann
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
