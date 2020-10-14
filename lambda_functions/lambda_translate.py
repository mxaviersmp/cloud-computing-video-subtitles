import json
import os
import boto3

TRANSLATE_BUCKET = os.environ.get('TRANSLATE_BUCKET')


def split_text(text, n=4500):
    t = text.split('\n')
    chunk = ''
    sentences = []
    for i in range(0, len(t), 4):
        chunk += '\n' + '\n'.join(t[i:i+4])
        if len(chunk) > n:
            sentences.append(chunk)
            chunk = ''
    if chunk:
        sentences.append(chunk)
        chunk = ''
    return sentences


def get_time_code( seconds ):
    # Format and return a string that contains the converted number of seconds into SRT format
    thund = int(seconds % 1 * 1000)
    tseconds = int( seconds )
    tsecs = ((float( tseconds) / 60) % 1) * 60
    tmins = int( tseconds / 60 ) % 60
    thours = int( (tseconds / 60) / 60 )
    return str( "%02d:%02d:%02d,%03d" % (thours, tmins, int(tsecs), thund ))


def json_to_vtt(transcribe_json):
    sentences = []
    sentence = []
    start = []
    end = []
    idx = 1
    for item in transcribe_json['results']['items']:
        if item['type'] == 'pronunciation':
            start.append(item['start_time'])
            end.append(item['end_time'])
            sentence.append(item['alternatives'][0]['content'])
        if item['type'] == 'punctuation':
            if item['alternatives'][0]['content'] in ['.', '?', '!']:
                sentence.append(item['alternatives'][0]['content'])
                try:
                    sentences.append({
                        'index': idx,
                        'start_time': get_time_code(float(start[0])),
                        'end_time': get_time_code(float(end[-1])),
                        'sentence': ' '.join(sentence)
                    })
                except IndexError as e:
                    print(e)
                sentence = []
                start = []
                end = []
                idx += 1
            else:
                sentence.append(item['alternatives'][0]['content'])
    transcript_timestamped = []
    for sent in sentences:
        transcript_timestamped.append(
            '{}\n{} --> {}\n{}\n'.format(
                sent['index'], sent['start_time'],
                sent['end_time'], sent['sentence']
            )
        )
    transcript_timestamped = '\n'.join(transcript_timestamped)
    transcript_timestamped = transcript_timestamped.strip()
    return transcript_timestamped


def fix_timestamp(x):
    if ' —> ' not in x:
        return x
    x = x.split()
    return ''.join(x[:2]) + ' --> ' + ''.join(x[-2:])


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
        transcript_text = json_to_vtt(json_content)

        translated_text = []
        for transcript_chunk in split_text(transcript_text):
            print('translating file')
            translated_chunk = translate.translate_text(
                Text=transcript_chunk,
                SourceLanguageCode='en',
                TargetLanguageCode='pt'
            )
            translated_text.append(translated_chunk['TranslatedText'])
        translated_text = '\n'.join(translated_text)
        translated_text = translated_text.strip().split('\n')
        translated_text = '\n'.join([fix_timestamp(l) for l in translated_text])

        _, file_name = os.path.split(file_name)
        file_name, _ = os.path.splitext(file_name)

        s3.Object(
            TRANSLATE_BUCKET, 'en/{}.vtt'.format(file_name)
        ).put(Body=transcript_text)
        s3.Object(
            TRANSLATE_BUCKET, 'pt/{}.vtt'.format(file_name)
        ).put(Body=translated_text)

    return {
        'statusCode': 200,
        'body': json.dumps('Translate Lambda finished!')
    }
