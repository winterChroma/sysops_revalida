import json
import uuid
import boto3
from datetime import datetime, timedelta
import os


dbRegion = os.environ['dbRegion']
dbName = os.environ['dbName']
client = boto3.client('dynamodb', region_name=dbRegion)

def lambda_handler(event, context):

    try:
        body = json.loads(event['body'])

        riderId = body["riderId"]
        bookingLocationN = str(body["bookingLocation"]["N"])
        bookingLocationW = str(body["bookingLocation"]["W"])
        targetLocationN = str(body["targetLocation"]["N"])
        targetLocationW = str(body["targetLocation"]["W"])
        state = "pending"

        rideId = str(uuid.uuid4())
        now = datetime.now() + timedelta(hours=8)
        timestamp = now.strftime("%Y-%m-%dT%H-%M-%S+8000")

        response = client.put_item(
            TableName = dbName,
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
                "timestamp": {
                    "S": timestamp
                },
                "datePendingState": {
                    "S": timestamp +"#"+ state
                }

            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "rideId": rideId,
                "state": state
            })
        }
    except:
        return {
            "statusCode": 400,
            "body": "Bad request"
        }
