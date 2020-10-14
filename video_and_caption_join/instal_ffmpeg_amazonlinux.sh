cd /usr/local/bin
sudo mkdir ffmpeg

cd ffmpeg
sudo wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
sudo mkdir ffmpeg-release-amd64-static
sudo tar xvf ffmpeg-release-amd64-static.tar.xz -C ffmpeg-release-amd64-static
mv ffmpeg-release-amd64-static/ffmpeg .

ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
exit