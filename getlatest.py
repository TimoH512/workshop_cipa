import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import decimal

dynamodb = boto3.resource('dynamodb')


def getlatest(event, context):
    table = dynamodb.Table(os.environ['TABLE_NAME'])

    #db.collection.find().limit(1).sort({$natural:-1})
    # result = table.query(KeyConditionExpression=Key('timestamp').eq('latest_entry_identifier'))
    result = table.scan()
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=DecimalEncoder)
    }
    return response


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)
