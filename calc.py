import json
from audioop import add
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
import time
from datetime import datetime

dynamodb = boto3.resource('dynamodb')


def calculation(event, context):
    nr1 = int(event['pathParameters']['nr1'])
    nr2 = int(event['pathParameters']['nr2'])
    requestbody = json.loads(event.get('body'))


    statuscode = 404

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
        return response

    statuscode = 200
    body = {
        "Summe": str(ressumm),
        "Differenz": str(resdiff),
        "Produkt": str(resprod),
        "Quotient": str(resquot),
        "requestbody": requestbody
    }

    response = {
        "statusCode": statuscode,
        "body": json.dumps(body)
    }

    addToTable(statuscode, body, ressumm, resdiff, resprod, resquot, nr1, nr2)
    return response


def addToTable(statuscode, body, ressumm,resdiff,resprod,resquot, nr1, nr2):
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


