import json
import boto3

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    riderType = event['pathParameters']["riderType"]
    riderId = event['pathParameters']["riderId"]

    body = json.loads(event['body'])
    location = body["location"]

    if(riderType=="riders"):
        pk = "PS#" + riderId
        riderTypeId = "passenderId"
    elif(riderType == "drivers"):
        pk = "DR#" + riderId
        riderTypeId = "driverId"
    
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
                "S": location
            },
            ":riderId": {
                "S": riderId
            }
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "response": "Location updated."
        })
    }
