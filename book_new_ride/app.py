import json
import uuid
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    body = json.loads(event['body'])

    riderId = body["riderId"]
    bookingLocationN = body["bookingLocation"]["N"]
    bookingLocationW = body["bookingLocation"]["W"]
    targetLocationN = body["targetLocation"]["N"]
    targetLocationW = body["targetLocation"]["W"]
    state = "pending"

    rideId = str(uuid.uuid4())

    response = client.put_item(
        TableName = "frab_revalida",
        Item = {
            "PK": {
                "S": "PS#" +    riderId
            },
            "SK": {
                "S": "RIDE#" + rideId
            },
            "rideId": {
                "S": rideId
            },
            "passengerId": {
                "S":    riderId
            },
            "state": {
                "S": state
            },
            "bookingLocation": {
                "M": {
                    "Longitude" : {
                        "S" : bookingLocationN
                    },
                    "Latitude" : {
                        "S" : bookingLocationW
                    }
                }
            },
            "targetLocation": {
                "M": {
                    "Longitude" : {
                        "S" : targetLocationN
                    },
                    "Latitude" : {
                        "S" : targetLocationW
                    }
                }
            },
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "rideId": rideId,
            "state": state
        })
    }
