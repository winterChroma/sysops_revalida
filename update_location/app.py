import json
import boto3
import uuid
from datetime import datetime, timedelta

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    try:

        riderType = event['pathParameters']["riderType"]
        riderId = event['pathParameters']["riderId"]

        body = json.loads(event['body'])

        if(riderType=="riders"):
            pk = "PS#" + riderId
            riderTypeId = "passengerId"
            locationText = "currentLocation"
            locationN = body["currentLocation"]["N"]
            locationW = body["currentLocation"]["W"]
            timestampType = "lastActive"
        elif(riderType == "drivers"):
            pk = "DR#" + riderId
            riderTypeId = "driverId"
            locationText = "updatedLocation"
            locationN = body["updatedLocation"]["N"]
            locationW = body["updatedLocation"]["W"]
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
                            "S" : locationN
                        },
                        "Latitude" : {
                            "S" : locationW
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
                locationText : {
                    "N": locationN,
                    "W": locationW
                },
                timestampType: timestamp
            })
        }

    except:
        return {
            "statusCode": 400,
            "body": "Bad request"
        }
