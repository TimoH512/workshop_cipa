import json
import datetime

def hello(event, context):
    current_time = datetime.datetime.now().time()
    body = {
        "message": "Hello World, the current time is " + str(current_time)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

