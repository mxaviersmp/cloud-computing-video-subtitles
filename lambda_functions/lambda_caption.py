import json
import os
import boto3
from urllib import parse, request


def create_uri(bucket_name, file_name=''):
    return 's3://{}/{}'.format(bucket_name, file_name)


def lambda_handler(event, context):

    if event:
        file_obj = event['Records'][0]
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])

        _, file_name = os.path.split(file_name)
        file_name, _ = os.path.splitext(file_name)

        orignal_video = create_uri('video-files-4124-8523-4476/original', '{}.mp4'.format(file_name))
        transcription = create_uri('transcribed-4124-8523-4476', '{}.json'.format(file_name))
        translation = create_uri('translated-4124-8523-4476', '{}.txt'.format(file_name))
        captioned_video = create_uri('video-files-4124-8523-4476/captioned', '{}.txt'.format(file_name))

        data = parse.urlencode({
            'original_video': orignal_video,
            'transcription': transcription,
            'translation': translation,
            'captioned_video': captioned_video
        })
        data = data.encode('ascii')

        url = "http://httpbin.org/post"
        request.urlopen(url, data)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
