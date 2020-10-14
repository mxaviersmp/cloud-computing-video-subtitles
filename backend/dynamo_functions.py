import logging
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


def retrieve_all_items(table_name):
    dynamo_client = boto3.client('dynamodb')
    try:
        response = dynamo_client.scan(
            TableName=table_name,
            Select='ALL_ATTRIBUTES'
        )
        return response['Items']
    except ClientError as e:
        logging.error(e)
        return False


def get_items(table_name, key, value):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    try:
        response = table.scan(
            FilterExpression=Key(key).eq(value)
        )
        return response['Items']
    except ClientError as e:
        logging.error(e)
        return False


def save_item(table_name, item, key, value):
    dynamo_client = boto3.client('dynamodb')
    try:
        dynamo_client.put_item(
            TableName=table_name,
            Item=item,
        )
        new_item = dynamo_client.get_item(
            TableName=table_name,
            Key={key: value}
        )['Item']
        return new_item
    except ClientError as e:
        logging.error(e)
        return False
