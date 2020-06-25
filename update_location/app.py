import json
import boto3
import uuid
from datetime import datetime, timedelta

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    riderType = event['pathParameters']["riderType"]
    riderId = event['pathParameters']["riderId"]

    body = json.loads(event['body'])

    if(riderType=="riders"):
        pk = "PS#" + riderId
        riderTypeId = "passengerId"
        location = "currentLocation"
        LocationN = body["currentLocation"]["N"]
        LocationW = body["currentLocation"]["W"]
        timestampType = "lastActive"
    elif(riderType == "drivers"):
        pk = "DR#" + riderId
        riderTypeId = "driverId"
        location = "updatedLocation"
        LocationN = body["updatedLocation"]["N"]
        LocationW = body["updatedLocation"]["W"]
        timestampType = "createdAt"
    
    locationId = str(uuid.uuid4())
    now = datetime.now() + timedelta(hours=8)
    timestamp = now.strftime("%Y-%m-%dT%H-%M-%S+8000")

    response = client.update_item(
        TableName = "frab_revalida",
        Key = {
            "PK": {
                "S": pk
            },
            "SK": {
                "S": "#PROFILE#" + riderId
            }
        },
        UpdateExpression="SET #loc=:loc, #riderTypeId=:riderId, locationId=:locationId, #ts=:ts",
        ExpressionAttributeNames={
            "#loc": "location",
            "#riderTypeId": riderTypeId,
            "#ts": "timestamp"
        },
        ExpressionAttributeValues={
            ":loc": {
                "M": {
                    "Longitude" : {
                        "S" : LocationN
                    },
                    "Latitude" : {
                        "S" : LocationW
                    }
                }
            },
            ":riderId": {
                "S": riderId
            },
            ":locationId": {
                "S": locationId
            },
            ":ts": {
                "S": timestamp
            }
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "locationId": locationId,
            location : {
                "N": LocationN,
                "W": LocationW
            },
            timestampType: timestamp
        })
    }
