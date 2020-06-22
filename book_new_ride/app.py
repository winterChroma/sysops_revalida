import json
import uuid
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    body = json.loads(event['body'])

    passenger = body["riderId"]
    startLocation = body["startLocation"]
    endLocation = body["endLocation"]
    status = "Finding a driver"

    rideId = str(uuid.uuid4())

    response = client.put_item(
        TableName = "frab_revalida",
        Item = {
            "PK": {
                "S": "PS#" + passenger
            },
            "SK": {
                "S": "RIDE#" + rideId
            },
            "rideId": {
                "S": rideId
            },
            "passengerId": {
                passenger
            },
            "status": {
                "S": status
            },
            "startLocation": {
                "S": startLocation
            },
            "endLocation": {
                "S": endLocation
            },
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "rideId": rideId
        })
    }
