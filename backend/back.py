from flask import Flask, request
import os
from s3_functions import upload_file
from dynamo_functions import save_item, get_items
import json

app = Flask(__name__)

VIDEOS_BUCKET = os.environ.get('VIDEOS_BUCKET')
VIDEOS_TABLE = os.environ.get('VIDEOS_TABLE')

@app.route('/send', methods=['POST'])
def send_videos():
    user_id = request.json.get('user_id')
    file_path = request.json.get('file_path')
    _, video_name = os.path.split(file_path)
    print(user_id, file_path, video_name)

    video_id = upload_file(file_path, VIDEOS_BUCKET)
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


@app.route('/list', methods=['POST'])
def list_videos():
    user_id = request.json.get('user_id')
    items = get_items(VIDEOS_TABLE, 'user_id', user_id)
    videos = []
    for d in items:
        info = dict()
        for k, v in d.items():
            info[k] = str(v)
        videos.append(info)
    return json.dumps(videos)


if __name__ == '__main__':
    app.run(debug=True)
