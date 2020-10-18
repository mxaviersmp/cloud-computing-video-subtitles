from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from s3_functions import upload_file
from dynamo_functions import save_item, get_items, retrieve_all_items
import json

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

VIDEOS_BUCKET = os.environ.get('VIDEOS_BUCKET')
VIDEOS_TABLE = os.environ.get('VIDEOS_TABLE')
FLASK_HOST = os.environ.get('FLASK_HOST')
FLASK_PORT = os.environ.get('FLASK_PORT')


@app.route('/send', methods=['POST'])
def send_videos():
    """Send a vídeo from a user to the S3

    Methods
    -------
    POST

    Request
    -------
    {
        "user_id": <id of the user>,
        "file_name": <name of file>
        "file": <the real video file>
    }

    Response
    --------
    {
        "status": 200
    }
    """
    
    user_id = request.form.get('user_id')
    user_email = request.form.get('user_email')
    file_name = request.form.get('file_name')
    file_video = request.files.get('file')
    
    video_id = upload_file(user_id, file_name, file_video, VIDEOS_BUCKET, 'original')
    video_info = {
        "video_id": {"S": video_id},
        "user_id": {"S": user_id},
        "user_email": {"S": user_email},
        "video_name": {"S": file_name},
        "finished": {"BOOL": False},
    }
    save_item(
        VIDEOS_TABLE, video_info,
        'video_id', {'S': video_info['video_id']['S']}
    )

    return json.dumps({'statusCode': 200})


@app.route('/list', methods=['GET'])
def list_videos():
    """Returns all videos from a user

    Methods
    -------
    GET

    Request
    -------
    {
        /list?id=user_id <id of the user>
    }

    Response
    -------
    [
        {
            "video_id": str,
            "video_name": str,
            "finished": bool,
            "duration": float,
            "transcription_words": float,
            "translation_words": float,
            "video_uri": str,
        },
        ...
    ]
    """
    user_id = request.args.get('id')
    items = get_items(VIDEOS_TABLE, 'user_id', user_id)
    videos = []
    if items:
        for d in items:
            info = dict()
            for k, v in d.items():
                info[k] = str(v)
            videos.append(info)
    return json.dumps(videos)


@app.route('/statistics', methods=['GET'])
def get_statistics():
    """Returns all videos

    Methods
    -------
    GET

    Request
    -------
    { }

    Response
    -------
    [
        {
            "video_id": str,
            "video_name": str,
            "finished": bool,
            "duration": float,
            "transcription_words": float,
            "translation_words": float,
        },
        ...
    ]
    """
    items = retrieve_all_items(VIDEOS_TABLE)
    videos = []
    if items:
        for d in items:
            info = dict()
            for k, v in d.items():
                info[k] = str([*v.values()][0])
            videos.append(info)
    return json.dumps(videos)


@app.route('/', methods=['GET'])
def health():
    return json.dumps("Healthy!")


if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)
