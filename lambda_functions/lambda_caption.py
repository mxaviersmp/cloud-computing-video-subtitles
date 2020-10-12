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

        original_video = 'video-files-4124-8523-4476/original/{}.mp4'.format(file_name)
        transcription = 'translated-4124-8523-4476/en/{}-en.vtt'.format(file_name)
        translation = 'translated-4124-8523-4476/pt/{}-pt.vtt'.format(file_name)
        captioned_video = 'video-files-4124-8523-4476/captioned/{}.mp4'.format(file_name)
        job_info = 'video-files-4124-8523-4476/info/{}.json'.format(file_name)

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
