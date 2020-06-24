import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    driverId = event['pathParameters']["driverId"]
    rideId = event['pathParameters']["rideId"]
    body = json.loads(event['body'])
    acceptLocationN = body["acceptLocation"]["N"]
    acceptLocationW = body["acceptLocation"]["W"]
    

    queryResponse = client.query(
        TableName = "frab_revalida",
        IndexName = "frab_inverted_index",
        Select = "SPECIFIC_ATTRIBUTES",
        ProjectionExpression="PK, SK",
        KeyConditionExpression="SK = :rideId",
        ExpressionAttributeValues={
            ":rideId": {
                "S": "RIDE#" + rideId
            }
        }
    )

    pk = queryResponse["Items"][0]["PK"]["S"]
    sk = queryResponse["Items"][0]["SK"]["S"]
    
    response = client.update_item(
        TableName = "frab_revalida",
        Key = {
            "PK": {
                "S": pk
            },
            "SK": {
                "S": sk
            }
        },
        UpdateExpression="SET driverId=:driverId, #state=:state",
        ExpressionAttributeNames={
            "#state": "state"
        },
        ExpressionAttributeValues={
            ":driverId": {
                "S": driverId
            },
            ":state": {
                "S": "accepted"
            }
        }
    )
    #########################subject to change
    response = client.update_item(
        TableName = "frab_revalida",
        Key = {
            "PK": {
                "S": "DR#" + driverId
            },
            "SK": {
                "S": "#PROFILE#" + driverId
            }
        },
        UpdateExpression=
        "SET #location=:location, #driverId=:driverId, #acceptlocation=:acceptlocation",
        ExpressionAttributeNames={
            "#location": "location",
            "#driverId": "driverId",
            "#acceptlocation": "acceptlocation"
        },
        ExpressionAttributeValues={
            ":acceptlocation": {
                "M": {
                    "Longitude" : {
                        "S" : acceptLocationN
                    },
                    "Latitude" : {
                        "S" : acceptLocationW
                    }
                }
            },
            ":location": {
                "M": {
                    "Longitude" : {
                        "S" : acceptLocationN
                    },
                    "Latitude" : {
                        "S" : acceptLocationW
                    }
                }
            },
            ":driverId": {
                "S": driverId
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
            "createdAt": "placeholder"
        })
    }
