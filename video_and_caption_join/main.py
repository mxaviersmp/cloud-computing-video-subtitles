from flask import Flask, jsonify, request, Response
import json
import os
import multiprocessing
import boto3
from VideoSubtitle import *

s3_client = boto3.client('s3')

API_FLASK_HOST = os.environ.get('API_FLASK_HOST')
API_FLASK_PORT = os.environ.get('API_FLASK_PORT')
LAMBDA_AUTH = os.environ.get('LAMBDA_AUTH')

app = Flask( __name__ )

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

@app.route('/video', methods=['POST'])
def storeVideo():

    if request.method == 'POST':

        data = request.get_json()

        if data['AUTH'] != AUTH:
             return jsonify(""), 401

        fileName = data['original_video'].split('.')[0].split('/')[-1]

        originalClipPath = downloadFileFromBucket( data['original_video'], fileName )
        subtitlesPtFilePath = downloadFileFromBucket( data['translation'], fileName )
        subtitlesEnFilePath = downloadFileFromBucket( data['transcription'], fileName )
        outputFilePath = './temp/captioned/{fileName}.mp4'.format( originalClipPath )

        job = multiprocessing.Process(
            target=start_job,
            args=(
                fileName, originalClipPath, subtitlesPtFilePath,
                subtitlesEnFilePath, outputFilePath
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
    salveFileToBucket( data['job_info'], fileName, './temp/jobInfo/{}.json'.format(fileName) )


if __name__ == '__main__':

    app.run( host=API_FLASK_HOST, port=API_FLASK_PORT )
