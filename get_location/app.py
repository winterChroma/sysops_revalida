import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    riderId = event['pathParameters']["riderId"]
    riderType = event['pathParameters']["riderType"]

    if(riderType == "riders"):
        locationText = "currentLocation"
        timestampText = "lastActive"
    elif(riderType == "drivers"):
        locationText = "updatedLocation"
        timestampText = "createdAt"
    else:
        return {
            "statusCode": 400,
            "body": "Bad request"
        }

    try:
        response = client.query(
            TableName = "frab_revalida",
            IndexName = "frab_inverted_index",
            Select = "SPECIFIC_ATTRIBUTES",
            ProjectionExpression="#loc, #ts, locationId",
            ExpressionAttributeNames={
                "#loc": "location",
                "#ts": "timestamp",
            },
            KeyConditionExpression="SK = :riderId",
            ExpressionAttributeValues={
                ":riderId": {
                    "S": "#PROFILE#" + riderId
                }
            }
        )
    except:
        return {
            "statusCode": 400,
            "body": "Bad request"
        }

    location = response["Items"][0]["location"]["M"]
    locationN = location["Longitude"]["S"]
    locationW = location["Latitude"]["S"]
    locationId = response["Items"][0]["locationId"]["S"]
    timestamp = response["Items"][0]["timestamp"]["S"]

    if(riderType == "riders"):
        return {
            "statusCode": 200,
            "body": json.dumps({
                "riderId": riderId,
                locationText: {
                    "N": locationN,
                    "W": locationW
                },
                timestampText: timestamp
            })
        }
    elif(riderType == "drivers"):
        return {
            "statusCode": 200,
            "body": json.dumps({
                "locationId": locationId,
                locationText: {
                    "N": locationN,
                    "W": locationW
                },
                timestampText: timestamp
            })
        }
    
