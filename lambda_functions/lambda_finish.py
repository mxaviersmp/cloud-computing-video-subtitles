import json
import os
import boto3

VIDEOS_TABLE = os.environ.get('VIDEOS_TABLE')
USERS_TABLE = os.environ.get('USERS_TABLE')
SOURCE_EMAIL = os.environ.get('SOURCE_EMAIL')

def lambda_handler(event, context):

    s3 = boto3.resource('s3')
    dynamo = boto3.client('dynamodb')
    ses = boto3.client('ses')

    if event:
        file_obj = event['Records'][0]
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])
        content_object = s3.Object(bucket_name, file_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        info = json.loads(file_content)

        video = dynamo.query(
            TableName=VIDEOS_TABLE,
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
            TableName=VIDEOS_TABLE,
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

        updated_user = dynamo.update_item(
            TableName=USERS_TABLE,
            Key={
                "username": username
            },
            UpdateExpression='SET #V = list_append(#V, :v)',
            ExpressionAttributeValues={
                ":v": {"L": [{"M": updated_video}]}
            },
            ExpressionAttributeNames={
                '#V': 'videos'
            },
            ReturnValues='ALL_NEW'
        )['Attributes']

        to_email = updated_user['email']['S']
        video_name = updated_video['video_name']['S']
        user_name = username['S']
        message = 'Hi {}, the video {} has been translated!'.format(
            user_name, video_name
        )

        try:
            ses = ses.send_email(
                Source=SOURCE_EMAIL,
                Destination={
                    'ToAddresses': [
                        to_email,
                    ]
                },
                Message={
                    'Subject': {
                        'Data': 'Video Translated by cloud-computing-video-subtitles'
                    },
                    'Body': {
                        'Text': {
                            'Data': message
                        }
                    }
                }
            )
        except ses.exceptions.MessageRejected:
            print('User email is not verified')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Finish Jod Lambda!')
    }
