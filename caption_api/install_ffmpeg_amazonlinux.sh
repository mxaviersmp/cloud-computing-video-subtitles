cd /usr/local/bin
mkdir ffmpeg

cd ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
mkdir ffmpeg-release-amd64-static
tar xvf ffmpeg-release-amd64-static.tar.xz -C ffmpeg-release-amd64-static --strip-components 1
mv ffmpeg-release-amd64-static/ffmpeg .

ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
exit