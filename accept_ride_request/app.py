import json
import boto3
from datetime import datetime, timedelta
import os


dbRegion = os.environ['dbRegion']
dbName = os.environ['dbName']
dbIndex = os.environ['dbIndex']

client = boto3.client('dynamodb', region_name=dbRegion)

def lambda_handler(event, context):

    driverId = event['pathParameters']["driverId"]
    rideId = event['pathParameters']["rideId"]
    body = json.loads(event['body'])
    acceptLocationN = str(body["acceptLocation"]["N"])
    acceptLocationW = str(body["acceptLocation"]["W"])
    
    

    queryResponse = client.query(
        TableName = dbName,
        IndexName = dbIndex,
        Select = "SPECIFIC_ATTRIBUTES",
        ProjectionExpression="PK, SK, #ts",
        KeyConditionExpression="SK = :rideId",
        ExpressionAttributeNames={
            "#ts": "timestamp"
        },
        ExpressionAttributeValues={
            ":rideId": {
                "S": "RIDE#" + rideId
            }
        }
    )

    pk = queryResponse["Items"][0]["PK"]["S"]
    sk = queryResponse["Items"][0]["SK"]["S"]
    timestamp = queryResponse["Items"][0]["timestamp"]["S"]
    
    response = client.update_item(
        TableName = dbName,
        Key = {
            "PK": {
                "S": pk
            },
            "SK": {
                "S": sk
            }
        },
        UpdateExpression="SET driverId=:driverId, #state=:state, acceptLocation=:acceptLocation, driverIdKey=:driverIdKey, stateDate=:stateDate REMOVE datePendingState",
        ExpressionAttributeNames={
            "#state": "state"
        },
        ExpressionAttributeValues={
            ":driverId": {
                "S": driverId
            },
            ":driverIdKey": {
                "S": "DR#" + driverId
            },
            ":state": {
                "S": "accepted"
            },
            ":stateDate": {
                "S": "accepted#" + timestamp
            },
            ":acceptLocation": {
                "M": {
                    "Longitude" : {
                        "S" : acceptLocationN
                    },
                    "Latitude" : {
                        "S" : acceptLocationW
                    }
                }
            }
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "rideId": rideId,
            "acceptLocation": {
                "N": acceptLocationN,
                "W": acceptLocationW
            },
            "createdAt": timestamp
        })
    }
