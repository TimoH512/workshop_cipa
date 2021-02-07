import json
import boto3
import os
import decimal

from boto3.dynamodb.conditions import Key, Attr


def getKey(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    key = event['pathParameters']['key']

    result = table.query(
        KeyConditionExpression=Key('timestamp').eq(key)
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }
    return response



#Rückgabe von DynamoDB umwandeln damit JSON die Daten verarbeiten kann
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)