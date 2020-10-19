import json
import os
import boto3

VIDEOS_TABLE = os.environ.get('VIDEOS_TABLE')
SOURCE_EMAIL = os.environ.get('SOURCE_EMAIL')


def create_object_url(bucket_name, file_name):
    return 'https://{}.s3.amazonaws.com/{}'.format(bucket_name, file_name)


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

        video_id = info['video_id']
        video_key = '/captioned/{}.mp4'.format(video_id)
        video_uri = create_object_url(bucket_name, video_key)

        video = dynamo.query(
            TableName=VIDEOS_TABLE,
            Select='ALL_ATTRIBUTES',
            KeyConditionExpression='#id = :vid',
            ExpressionAttributeValues={
                ":vid": {"S": video_id}
            },
            ExpressionAttributeNames={
                '#id': 'video_id'
            },
        )['Items'][0]

        updated_video = dynamo.update_item(
            TableName=VIDEOS_TABLE,
            Key={
                "video_id": {"S": video_id}
            },
            UpdateExpression='SET #U = :u, #D = :d, #T1 = :t1, #T2 = :t2, #F = :f',
            ExpressionAttributeValues={
                ":u": {"S": str(video_uri)},
                ":d": {"N": str(info['duration'])},
                ":t1": {"N": str(info['transcription_words'])},
                ":t2": {"N": str(info['translation_words'])},
                ':f': {"BOOL": True}
            },
            ExpressionAttributeNames={
                '#U': 'video_uri',
                '#D': 'duration',
                '#T1': 'transcription_words',
                '#T2': 'translation_words',
                '#F': 'finished',
            },
            ReturnValues='ALL_NEW'
        )['Attributes']

        video_name = updated_video['video_name']['S']
        to_email = updated_video['user_email']['S']
        message = 'Hi, the video {} has been translated!'.format(
            video_name
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
            ses.verify_email_identity(
                EmailAddress=to_email
            )

    return {
        'statusCode': 200,
        'body': json.dumps('FinishJob Lambda Successful!')
    }
