import json

def calculation(event, context):
    nr1 = event['pathParameters']['nr1']
    nr2 = event['pathParameters']['nr2']
    body = {
        "Zahl1": nr1,
        "Zahl2": nr2
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

