import json
import os
import boto3


def create_uri(bucket_name, file_name=''):
    return 's3://{}/{}'.format(bucket_name, file_name)


def split_text(text, n=4500):
    words = iter(text.split())
    lines, current = [], next(words)
    for word in words:
        if len(current) + 1 + len(word) > n:
            lines.append(current)
            current = word
        else:
            current += " " + word
    lines.append(current)
    return lines


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    translate = boto3.client('translate')
    
    if event:
        file_obj = event['Records'][0]
        bucket_name = str(file_obj['s3']['bucket']['name'])
        file_name = str(file_obj['s3']['object']['key'])
        
        content_object = s3.Object(bucket_name, file_name)
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        transcript_text = json_content['results']['transcripts'][0]['transcript']
        
        translated_text = []
        for transcript_chunk in split_text(transcript_text):
            print('translating file')
            translated_chunk = translate.translate_text(
                Text=transcript_chunk,
                SourceLanguageCode='en',
                TargetLanguageCode='pt'
            )
            translated_text.append(translated_chunk['TranslatedText'])
        translated_text = ' '.join(translated_text)

        
        _, file_name = os.path.split(file_name)
        file_name, _ = os.path.splitext(file_name)

        s3.Object('translated-4124-8523-4476', '{}.txt'.format(file_name)).put(Body=translated_text)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
