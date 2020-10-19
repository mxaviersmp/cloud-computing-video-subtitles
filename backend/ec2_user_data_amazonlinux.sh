#!/bin/bash

sudo yum update -y
sudo yum install git -y
git clone https://github.com/flych3r/cloud-computing-video-subtitles.git
cd cloud-computing-video-subtitles/backend
sudo yum install python3 -y
sudo python3 -m pip install -r requirements.txt
export FLASK_HOST=0.0.0.0
export FLASK_PORT=8080
export VIDEOS_BUCKET=<s3-bucket>
export VIDEOS_TABLE=<dynamodb-table>
python3 back.py
