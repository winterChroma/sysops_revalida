import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    rideId = event['pathParameters']["rideId"]

    response = client.query(
        TableName = "frab_revalida",
        IndexName = "frab_inverted_index",
        Select = "SPECIFIC_ATTRIBUTES",
        ProjectionExpression="#S, #D",
        ExpressionAttributeNames={
            "#S" : "state",
            "#D" : "driverId"
        },
        KeyConditionExpression="SK = :rideId",
        ExpressionAttributeValues={
            ":rideId": {
                "S": "RIDE#" + rideId
            }
        }
    )

    state = response["Items"][0]["state"]["S"]
    driverId = response["Items"][0]["driverId"]["S"]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "rideId": rideId,
            "state": state,
            "driverId": driverId
        })
    }
