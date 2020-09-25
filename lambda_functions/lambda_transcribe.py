import json
import os
import boto3

def create_uri(bucket_name, file_name):
    return 's3://{}/{}'.format(bucket_name, file_name)


def lambda_handler(event, context):
    transcribe = boto3.client('transcribe')
    
    if event:
        file_obj = event['Records'][0]
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])
        s3_uri = create_uri(bucket_name, file_name)
        
        _, file_name = os.path.split(file_name)
        file_name, file_ext = os.path.splitext(file_name)
        file_ext = file_ext[1:]
        
        print('started transcription for {}'.format(file_name))
        transcribe.start_transcription_job(
            TranscriptionJobName=file_name,
            LanguageCode='en-US',
            MediaFormat=file_ext,
            Media={
                'MediaFileUri': s3_uri
            },
            OutputBucketName='transcribed-4124-8523-4476'
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
