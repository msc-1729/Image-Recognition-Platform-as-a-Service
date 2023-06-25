import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import *

# def get_queue_url():
#     sqs_client = boto3.client("sqs")
#     response = sqs_client.get_queue_url(
#         QueueName="ouputQueue",
#     )
#     return response["QueueUrl"]
    
# def send_message(message):
#     sqs_client = boto3.client("sqs")

#     response = sqs_client.send_message(
#         QueueUrl=get_queue_url(),
#         MessageBody=json.dumps(message)
#     )
#     print(response)

    
def lambda_handler(event, context):
    # TODO implement
    name = event['name'].strip()
    requestKey = event['requestKey'].strip()
    print(name, requestKey)
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('cse546')
    
    response = table.scan(FilterExpression=Attr('name').eq(str(name)))
    print(response)
    data = response['Items']
    print(data)
    res = []
    for record in data:
        record['id'] = float(record['id'])
        res.append({str(requestKey): record})
    print(res)
    return res
    