#!/bin/bash

sudo yum update -y
sudo yum install git -y
git clone https://github.com/flych3r/cloud-computing-video-subtitles.git
cd cloud-computing-video-subtitles/caption_api
sudo bash install_ffmpeg_amazonlinux.sh
sudo bash install_imagemagick_amazonlinux.sh
sudo bash install_requirements_amazonlinux.sh
export API_FLASK_HOST=0.0.0.0
export API_FLASK_PORT=8080
python3 main.py