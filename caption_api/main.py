from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json
import os
import multiprocessing
import boto3
from VideoSubtitle import *

from dotenv import load_dotenv
load_dotenv()

s3_client = boto3.client('s3')

API_FLASK_HOST = os.environ.get('API_FLASK_HOST')
API_FLASK_PORT = os.environ.get('API_FLASK_PORT')

app = Flask( __name__ )
CORS(app)

if not os.path.exists('temp'):
    os.mkdir('./temp')
    os.mkdir('./temp/info')
    os.mkdir('./temp/original')
    os.mkdir('./temp/captioned')
    os.mkdir('./temp/pt')
    os.mkdir('./temp/en')

def downloadFileFromBucket( bucketUri, fileName ):

    bucketName =  bucketUri.split('/')[0]
    extension = bucketUri.split('.')[1]

    fileName = "{}/{}.{}".format(bucketUri.split('/')[1], fileName, extension)
    filePath = './temp/{}'.format(fileName)

    s3_client.download_file( bucketName, fileName, filePath )

    return filePath

def salveFileToBucket( bucketUri, fileName, filePath ):

    bucketName =  bucketUri.split('/')[0]
    extension = bucketUri.split('.')[1]

    fileName = "{}/{}.{}".format(bucketUri.split('/')[1], fileName, extension)

    s3_client.upload_file( filePath, bucketName, fileName )


@app.route('/', methods=['GET'])
def health():
    return jsonify("Healthy!"), 200


@app.route('/video', methods=['POST'])
def storeVideo():

    if request.method == 'POST':

        data = request.get_json()

        fileName = data['original_video'].split('.')[0].split('/')[-1]

        originalClipPath = downloadFileFromBucket( data['original_video'], fileName )
        subtitlesPtFilePath = downloadFileFromBucket( data['translation'], fileName )
        subtitlesEnFilePath = downloadFileFromBucket( data['transcription'], fileName )
        outputFilePath = './temp/captioned/{}.mp4'.format( fileName )

        job = multiprocessing.Process(
            target=start_job,
            args=(
                fileName, data, originalClipPath,
                subtitlesPtFilePath, subtitlesEnFilePath, outputFilePath
            )
        )
        job.start()

        return jsonify("Succesfully started job"), 201
    else:
        return jsonify(""), 400


def start_job(
    fileName, data, originalClipPath,
    subtitlesPtFilePath, subtitlesEnFilePath, outputFilePath
):
    vs = VideoSubtitle()

    job_info = vs.createAnnotatedVideo(
        fileName, originalClipPath, subtitlesPtFilePath,
        subtitlesEnFilePath, outputFilePath
    )

    with open('./temp/info/{}.json'.format(fileName), 'w') as outfile:
        json.dump(job_info, outfile)

    salveFileToBucket( data['captioned_video'], fileName, outputFilePath )
    salveFileToBucket( data['job_info'], fileName, './temp/info/{}.json'.format(fileName) )


if __name__ == '__main__':
    app.run( host=API_FLASK_HOST, port=API_FLASK_PORT )
