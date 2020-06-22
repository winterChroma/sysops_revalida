import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    rideId = event['pathParameters']["rideId"]

    response = client.query(
        TableName = "frab_revalida",
        IndexName = "frab_inverted_index",
        Select = "SPECIFIC_ATTRIBUTES",
        ProjectionExpression="#S",
        ExpressionAttributeNames={
            "#S" : "status"
        },
        KeyConditionExpression="SK = :rideId",
        ExpressionAttributeValues={
            ":rideId": {
                "S": "RIDE#" + rideId
            }
        }
    )

    status = response["Items"][0]["status"]["S"]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": status
        })
    }
