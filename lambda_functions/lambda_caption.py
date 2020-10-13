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
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])

        _, file_name = os.path.split(file_name)
        file_name, _ = os.path.splitext(file_name)
        file_name = file_name.replace('-pt', '')

        original_video = '{}/original/{}.mp4'.format(VIDEO_BUCKET, file_name)
        transcription = '{}/en/{}-en.vtt'.format(TRANSLATE_BUCKET, file_name)
        translation = '{}/pt/{}-pt.vtt'.format(TRANSLATE_BUCKET, file_name)
        captioned_video = '{}/captioned/{}.mp4'.format(VIDEO_BUCKET, file_name)
        job_info = '{}/info/{}.json'.format(VIDEO_BUCKET, file_name)

        data = parse.urlencode({
            'original_video': original_video,
            'transcription': transcription,
            'translation': translation,
            'captioned_video': captioned_video,
            'job_info': job_info
        })
        data = data.encode('ascii')

        url = "http://httpbin.org/post"
        response = request.urlopen(url, data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Caption Lambda!')
    }
