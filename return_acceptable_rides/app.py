import json
import boto3
import os


dbRegion = os.environ['dbRegion']
dbName = os.environ['dbName']
dbIndex = os.environ['dbIndex']

client = boto3.client('dynamodb', region_name=dbRegion)

def lambda_handler(event, context):

    response = client.query(
       TableName = dbName,
       IndexName = dbIndex,
       Select = "SPECIFIC_ATTRIBUTES",
       ProjectionExpression="rideId, bookingLocation",
       Limit=5,
       KeyConditionExpression="#s = :pendingState",
       ExpressionAttributeNames={
           "#s": "state"
       },
       ExpressionAttributeValues={
           ":pendingState": {
               "S": "pending"
           }
       }
    )

    payload=[]

    for item in response["Items"]:
        ride = {
            "rideId": item["rideId"]["S"],
            "currentLocation": {
                "N": item["bookingLocation"]["M"]["Latitude"]["S"],
                "W": item["bookingLocation"]["M"]["Longitude"]["S"]
            }
        }
        payload.append(ride)

    return {
        "statusCode": 200,
        "body": json.dumps(
            payload
        )
    }