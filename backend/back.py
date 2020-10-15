from flask import Flask, request
from flask_cors import CORS
import os
from s3_functions import upload_file
from dynamo_functions import save_item, get_items, retrieve_all_items
import json

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
        "file_path": <path to the file>
    }

    Response
    --------
    {
        "status": 200
    }
    """
    user_id = request.json.get('user_id')
    file_path = request.json.get('file_path')
    _, video_name = os.path.split(file_path)

    video_id = upload_file(user_id, file_path, VIDEOS_BUCKET, 'original')
    video_info = {
        "video_id": {"S": video_id},
        "user_id": {"S": user_id},
        "video_name": {"S": video_name},
        "finished": {"BOOL": False}
    }
    save_item(
        'videos_table', video_info,
        'video_id', {'S': video_info['video_id']['S']}
    )

    return json.dumps({'status': 200})


@app.route('/list', methods=['GET'])
def list_videos():
    """Returns all videos from a user

    Methods
    -------
    GET

    Request
    -------
    {
        "user_id": <id of the user>
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
        },
        ...
    ]
    """
    user_id = request.json.get('user_id')
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


if __name__ == '__main__':
    app.run(host=FLASK_HOST, port=FLASK_PORT)
