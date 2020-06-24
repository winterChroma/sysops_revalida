import json
import boto3

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
    elif(riderType == "drivers"):
        pk = "DR#" + riderId
        riderTypeId = "driverId"
        location = "updatedLocation"
        LocationN = body["updatedLocation"]["N"]
        LocationW = body["updatedLocation"]["W"]
    
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
        UpdateExpression="SET #loc=:loc, #riderTypeId=:riderId",
        ExpressionAttributeNames={
            "#loc": "location",
            "#riderTypeId": riderTypeId
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
            }
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            location : {
                "N": LocationN,
                "W": LocationW
            }

        })
    }
