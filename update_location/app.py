import json
import boto3
import uuid
from datetime import datetime, timedelta
from geopy.distance import distance
import os


dbRegion = os.environ['dbRegion']
dbName = os.environ['dbName']
dbIndex = os.environ['dbIndex']

client = boto3.client('dynamodb', region_name=dbRegion)

def lambda_handler(event, context):

    try:

        riderType = event['pathParameters']["riderType"]
        riderId = event['pathParameters']["riderId"]

        body = json.loads(event['body'])

        if(riderType=="riders"):
            pk = "PS#" + riderId
            riderTypeId = "passengerId"
            locationText = "currentLocation"
            locationN = str(body["currentLocation"]["N"])
            locationW = str(body["currentLocation"]["W"])
            timestampType = "lastActive"
        elif(riderType == "drivers"):
            pk = "DR#" + riderId
            riderTypeId = "driverId"
            locationText = "updatedLocation"
            locationN = str(body["updatedLocation"]["N"])
            locationW = str(body["updatedLocation"]["W"])
            timestampType = "createdAt"
        
        locationId = str(uuid.uuid4())
        now = datetime.now() + timedelta(hours=8)
        timestamp = now.strftime("%Y-%m-%dT%H-%M-%S+8000")

        response = client.update_item(
            TableName = dbName,
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

        if(riderType == "drivers"):
            stateUpdateResponse = client.query(
                TableName = dbName,
                IndexName = dbIndex,
                KeyConditionExpression = "driverIdKey= :pk",
                ExpressionAttributeValues= {
                    ":pk": {
                        "S": pk
                    }
                },
                Limit=1
            )

            stateDate = stateUpdateResponse["Items"][0]["stateDate"]["S"]
            state = stateDate.split("#")[0]
            date = stateDate.split("#")[1]
            pk = stateUpdateResponse["Items"][0]["PK"]["S"]
            sk = stateUpdateResponse["Items"][0]["SK"]["S"]

            if(state == "accepted"):
                bookingLocation = stateUpdateResponse["Items"][0]["bookingLocation"]["M"]
                bookingLocationN = bookingLocation["Longitude"]["S"]
                bookingLocationW = bookingLocation["Latitude"]["S"]
                dist = distance((locationN, locationW), (bookingLocationN, bookingLocationW)).m
                if(dist <= 20.0):
                    inProgressResponse = client.update_item(
                        TableName = dbName,
                        Key = {
                            "PK": {
                                "S": pk
                            },
                            "SK": {
                                "S": sk
                            }
                        },
                        UpdateExpression="SET #state=:state, stateDate=:stateDate",
                        ExpressionAttributeNames={
                            "#state": "state"
                        },
                        ExpressionAttributeValues={
                            ":state": {
                                "S": "in_progress"
                            },
                            ":stateDate": {
                                "S": "in_progress#"+date
                            }
                        }
                    )
                    
            if(state == "in_progress"):
                targetLocation = stateUpdateResponse["Items"][0]["targetLocation"]["M"]
                targetLocationN = targetLocation["Longitude"]["S"]
                targetLocationW = targetLocation["Latitude"]["S"]
                dist = distance((locationN, locationW), (targetLocationN, targetLocationW)).m
                if(dist <= 20.0):
                    completeSuccessResponse = client.update_item(
                        TableName = dbName,
                        Key = {
                            "PK": {
                                "S": pk
                            },
                            "SK": {
                                "S": sk
                            }
                        },
                        UpdateExpression="SET #state=:state REMOVE stateDate",
                        ExpressionAttributeNames={
                            "#state": "state"
                        },
                        ExpressionAttributeValues={
                            ":state": {
                                "S": "complete_success"
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
