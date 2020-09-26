import json
import os
import boto3
from urllib import parse, request

VIDEO_BUCKET = os.environ.get('VIDEO_BUCKET')
TRANSCRIBE_BUCKET = os.environ.get('TRANSCRIBE_BUCKET')
TRANSLATE_BUCKET = os.environ.get('TRANSLATE_BUCKET')

def create_uri(bucket_name, file_name=''):
    return 's3://{}/{}'.format(bucket_name, file_name)


def lambda_handler(event, context):

    if event:
        file_obj = event['Records'][0]
        file_name = str(file_obj['s3']['object']['key'])

        _, file_name = os.path.split(file_name)
        file_name, _ = os.path.splitext(file_name)

        original_video = create_uri(
            '{}/original'.format(VIDEO_BUCKET), '{}.mp4'.format(file_name)
        )
        transcription = create_uri(
            TRANSCRIBE_BUCKET, '{}.json'.format(file_name)
        )
        translation = create_uri(
            TRANSLATE_BUCKET, '{}.txt'.format(file_name)
        )
        captioned_video = create_uri(
            '{}/captioned'.format(VIDEO_BUCKET), '{}.txt'.format(file_name)
        )

        data = parse.urlencode({
            'original_video': original_video,
            'transcription': transcription,
            'translation': translation,
            'captioned_video': captioned_video
        })
        data = data.encode('ascii')

        url = "http://httpbin.org/post"
        request.urlopen(url, data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Caption Lambda!')
    }
