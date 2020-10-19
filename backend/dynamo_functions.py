import logging
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError


def retrieve_all_items(table_name):
    """Scans and retrieves all items from a DynamoDB table

    Parameters
    ----------
    table_name : str
        name of the table to scan

    Returns
    -------
    dict
        all items in the table
    """
    dynamo_client = boto3.client('dynamodb', region_name='us-east-1')
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
    """Retrieves all items from a DynamoDB table with key==value

    Parameters
    ----------
    table_name : str
        name of the table
    key : str
        item key to filter
    value : str
        value of the key

    Returns
    -------
    dict
        all items from the table that the atribute key==value
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
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
    """Saves an item on a DynamoDB table

    Parameters
    ----------
    table_name : str
        name of the table
    item : dict
        item to save on the table
    key : str
        item primary key
    value : str
        item pk value

    Returns
    -------
    dict
        item inserted on the table
    """
    dynamo_client = boto3.client('dynamodb', region_name='us-east-1')
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
