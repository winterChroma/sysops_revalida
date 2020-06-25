import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    response = client.query(
       TableName = "frab_revalida",
       IndexName = "frab_pending_rides",
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