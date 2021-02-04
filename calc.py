import json
from decimal import Decimal
import boto3
import os
import time

dynamodb = boto3.resource('dynamodb')


def calculation(event, context):
    # Pfad Parameter auslesen
    nr1 = int(event['pathParameters']['nr1'])
    nr2 = int(event['pathParameters']['nr2'])

    # JSON aus Request Body auslesen
    requestbody = json.loads(event.get('body'))
    requestbodynr1 = requestbody['nr1']
    requestbodynr2 = requestbody['nr2']

    try:
        ressumm = nr1 + nr2
        resdiff = nr1 - nr2
        resprod = nr1 * nr2
        resquot = nr1 / nr2
    except ZeroDivisionError:
        statuscode = 400
        body = {"message": "Zero Division Error"}
        response = {
            "statusCode": statuscode,
            "body": json.dumps(body)
        }
        addToTable(statuscode, body, ressumm, resdiff, resprod, resquot, nr1, nr2)
        return response

    statuscode = 200
    body = {
        "Summe": str(ressumm),
        "Differenz": str(resdiff),
        "Produkt": str(resprod),
        "Quotient": str(resquot),
        "requestbody": requestbody,
        "requestbodynr1": requestbodynr1,
        "requestbodynr2": requestbodynr2
    }

    response = {
        "statusCode": statuscode,
        "body": json.dumps(body)
    }

    addToTable(statuscode, body, ressumm, resdiff, resprod, resquot, nr1, nr2)
    return response


# Eintrag in die DynamoDB hinzufügen
def addToTable(statuscode, body, ressumm, resdiff, resprod, resquot, nr1, nr2):
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    item = {
        'timestamp': str(time.time()),
        'statuscode': str(statuscode),
        'ressumm': Decimal(str(ressumm)),
        'resdiff': Decimal(str(resdiff)),
        'resprod': Decimal(str(resprod)),
        'resquot': Decimal(str(resquot)),
        'nr1': nr1,
        'nr2': nr2,
    }

    table.put_item(Item=item)
