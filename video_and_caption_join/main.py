from flask import Flask, jsonify, request, Response
import json
import os
import boto3
from VideoSubtitle import *

s3_client = boto3.client('s3')

API_FLASK_HOST = 'localhost' #os.environ.get('API_FLASK_HOST')
API_FLASK_PORT = 4441 #os.environ.get('API_FLASK_PORT')

app = Flask( __name__ )

def downloadFileFromBucket( bucketUri, fileName ):

    bucketName =  bucketUri.split('/')[0]
    extension = bucketUri.split('.')[1]

    fileName = "{}/{}.{}".format(bucketUri.split(1), fileName, extension)
    filePath = './temp/{}'.format(fileName)

    s3_client.download_file( bucketName, fileName, filePath )

    return filePath

def salveFileToBucket( bucketUri, fileName, filePath ):

    bucketName =  bucketUri.split('/')[0]
    extension = bucketUri.split('.')[1]

    fileName = "{}.{}".format(fileName, extension)

    s3_client.upload_file( filePath, bucketName, fileName )

@app.route('/video', methods=['POST'])
def storeVideo():

    if request.method == 'POST':

        data = request.get_json()

        vs = VideoSubtitle()

        fileName = 'tom' #data['original_video'].split('.')[0].split('/')[-1]

        originalClipPath = './test/tom.mp4' #downloadFileFromBucket( data['original_video'], fileName )
        subtitlesPtFilePath = './test/tom-pt.vtt' #downloadFileFromBucket( data['translation'], fileName )
        subtitlesEnFilePath = './test/tom-en.vtt' #downloadFileFromBucket( data['transcription'], fileName )
        outputFilePath = './test/test.mp4' #'./temp/captioned/{fileName}.mp4'.format( originalClipPath )

        job_info = vs.createAnnotatedVideo( originalClipPath, subtitlesPtFilePath, subtitlesEnFilePath, outputFilePath )

        with open('./temp/info/{}.json'.format(fileName), 'w') as outfile:
            json.dump(job_info, outfile)

        #salveFileToBucket( data['captioned_video'], fileName, outputFilePath )
        #salveFileToBucket( data['job_info'], fileName, './temp/jobInfo/{}.json'.format(fileName) )

        return jsonify("Succesfully stored video"), 201

    else:

        return jsonify(""), 400

if __name__ == '__main__':

    app.run( host=API_FLASK_HOST, port=API_FLASK_PORT )