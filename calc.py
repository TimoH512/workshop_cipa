import json

def calculation(event, context):
    
    body = {
        "message": "Test"
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

