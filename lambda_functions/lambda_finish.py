import json
import os
import boto3


def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    dynamo = boto3.client('dynamodb')

    if event:
        file_obj = event['Records'][0]
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])
        content_object = s3.Object(bucket_name, file_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        info = json.loads(file_content)

        video = dynamo.query(
            TableName='videos_table',
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression='#id = :vid',
            ExpressionAttributeValues={
                ":vid": {"S": info['id']}
            },
            ExpressionAttributeNames={
                '#id': 'video_id'
            },
        )['Items'][0]

        updated_video = dynamo.update_item(
            TableName='videos_table',
            Key={
                "video_id": video['video_id']
            },
            UpdateExpression='SET #D = :d, #T1 = :t1, #T2 = :t2, #F = :f',
            ExpressionAttributeValues={
                ":d": {"N": str(info['duration'])},
                ":t1": {"N": str(info['transcription_words'])},
                ":t2": {"N": str(info['translation_words'])},
                ':f': {"BOOL": True}
            },
            ExpressionAttributeNames={
                '#D': 'duration',
                '#T1': 'transcription_words',
                '#T2': 'translation_words',
                '#F': 'finished',
            },
            ReturnValues='ALL_NEW'
        )['Attributes']

        username = updated_video['username']
        del updated_video['username']

        print(username)

        dynamo.update_item(
            TableName='users_table',
            Key={
                "username": username
            },
            UpdateExpression='SET #V = list_append(#V, :v)',
            ExpressionAttributeValues={
                ":v": {"L": [{"M": updated_video}]}
            },
            ExpressionAttributeNames={
                '#V': 'videos'
            }
        )

        print(updated_video)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Finish Jod Lambda!')
    }
