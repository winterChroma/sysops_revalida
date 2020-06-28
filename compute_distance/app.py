import json
import boto3
from geopy.distance import distance
import os


dbRegion = os.environ['dbRegion']
dbName = os.environ['dbName']
dbIndex = os.environ['dbIndex']

client = boto3.client('dynamodb', region_name=dbRegion)

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
    try:
        driverResponse = client.query(
            TableName = dbName,
            IndexName = dbIndex,
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
    except:
        return {
            "statusCode": 400,
            "body": "Driver location not found."
        }


    # get driver location
    try:
        riderResponse = client.query(
            TableName = dbName,
            IndexName = dbIndex,
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
    except:
        return {
            "statusCode": 400,
            "body": "Rider location not found"
        }

    driverLocation = driverResponse["Items"][0]["location"]["M"]
    driverLocationN = driverLocation["Longitude"]["S"]
    driverLocationW = driverLocation["Latitude"]["S"]
    riderLocation = riderResponse["Items"][0]["location"]["M"]
    riderLocationN = riderLocation["Longitude"]["S"]
    riderLocationW = riderLocation["Latitude"]["S"]
    
    dist = distance((driverLocationN, driverLocationW), (riderLocationN, riderLocationW)).m
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "distance": dist
        })
    }
