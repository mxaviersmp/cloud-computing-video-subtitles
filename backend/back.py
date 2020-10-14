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

    return {'status': 200}


@app.route('/list', methods=['GET'])
def list_videos():
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
    app.run(debug=True, host=FLASK_HOST, port=FLASK_PORT)
