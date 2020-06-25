import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")


def lambda_handler(event, context):

    rideId = event['pathParameters']["rideId"]

    try:
        response = client.query(
            TableName="frab_revalida",
            IndexName="frab_inverted_index",
            Select="SPECIFIC_ATTRIBUTES",
            ProjectionExpression="#S, #D",
            ExpressionAttributeNames={
                "#S": "state",
                "#D": "driverId"
            },
            KeyConditionExpression="SK = :rideId",
            ExpressionAttributeValues={
                ":rideId": {
                    "S": "RIDE#" + rideId
                }
            }
        )

        payload = {
            "rideId": rideId,
            "state": response["Items"][0]["state"]["S"]
        }
        try:
            payload["driverId"] = response["Items"][0]["driverId"]["S"]
            return {
                "statusCode": 200,
                "body": json.dumps(payload)
            }
        except:  
            return {
                "statusCode": 200,
                "body": json.dumps(payload)
            }
    except:
        return {
            "statusCode": 400,
            "body": "Bad request"
        }
