import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    driverId = event['pathParameters']["driverId"]
    rideId = event['pathParameters']["rideId"]

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
        UpdateExpression="SET driverId=:driverId, #status=:status",
        ExpressionAttributeNames={
            "#status": "status"
        },
        ExpressionAttributeValues={
            ":driverId": {
                "S": driverId
            },
            ":status": {
                "S": "On going"
            }
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "response": "Ride accepted."
        })
    }
