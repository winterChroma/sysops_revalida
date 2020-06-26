import json
import boto3
from geopy.distance import distance

client = boto3.client('dynamodb', region_name="ap-southeast-1")

def lambda_handler(event, context):

    driverId = event['pathParameters']["driverId"]

    try:
        body = json.loads(event['body'])
        riderId = body["riderId"]
    except:
        return {
            "statusCode": 400,
            "body": "Bad request"
        }

    # get driver location
    driverResponse = client.query(
        TableName = "frab_revalida",
        IndexName = "frab_inverted_index",
        Select = "SPECIFIC_ATTRIBUTES",
        ProjectionExpression="#loc",
        ExpressionAttributeNames={
            "#loc": "location",
        },
        KeyConditionExpression="SK = :driverId",
        ExpressionAttributeValues={
            ":driverId": {
                "S": "#PROFILE#" + driverId
            }
        }
    )

    # get rider location
    riderResponse = client.query(
        TableName = "frab_revalida",
        IndexName = "frab_inverted_index",
        Select = "SPECIFIC_ATTRIBUTES",
        ProjectionExpression="#loc",
        ExpressionAttributeNames={
            "#loc": "location",
        },
        KeyConditionExpression="SK = :riderId",
        ExpressionAttributeValues={
            ":riderId": {
                "S": "#PROFILE#" + riderId
            }
        }
    )

    try:
        driverLocation = driverResponse["Items"][0]["location"]["M"]
        driverLocationN = driverLocation["Longitude"]["S"]
        driverLocationW = driverLocation["Latitude"]["S"]
    except:
        return {
            "statusCode": 400,
            "body": "Driver location not found."
        }
    try:
        riderLocation = riderResponse["Items"][0]["location"]["M"]
        riderLocationN = riderLocation["Longitude"]["S"]
        riderLocationW = riderLocation["Latitude"]["S"]
    except:
        return {
            "statusCode": 400,
            "body": "Rider location not found"
        }
    
    dist = distance((driverLocationN, driverLocationW), (riderLocationN, riderLocationW)).m
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "distance": dist
        })
    }
