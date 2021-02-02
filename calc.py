import json


def calculation(event, context):
    nr1 = int(event['pathParameters']['nr1'])
    nr2 = int(event['pathParameters']['nr2'])

    try:
        ressumm = nr1 + nr2
        resdiff = nr1 - nr2
        resprod = nr1 * nr2
        resquot = nr1 / nr2
    except ZeroDivisionError:
        body = {"message": "Zero Division Error"}
        response = {
            "statusCode": 400,
            "body": json.dumps(body)
        }
        return response

    body = {
        "Summe": str(ressumm),
        "Differenz": str(resdiff),
        "Produkt": str(resprod),
        "Quotient": str(resquot)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
