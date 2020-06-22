import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    riderId = event['pathParameters']["riderId"]

    response = client.query(
        TableName = "frab_revalida",
        IndexName = "frab_inverted_index",
        Select = "SPECIFIC_ATTRIBUTES",
        ProjectionExpression="#loc",
        ExpressionAttributeNames={
            "#loc": "location"
        },
        KeyConditionExpression="SK = :riderId",
        ExpressionAttributeValues={
            ":riderId": {
                "S": "#PROFILE#" + riderId
            }
        }
    )

    location = response["Items"][0]["location"]["S"]

    return {
        "statusCode": 200,
        "body": json.dumps({
            "location": location
        })
    }
