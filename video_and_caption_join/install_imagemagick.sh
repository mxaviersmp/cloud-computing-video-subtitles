#!/bin/bash

if !  sudo apt update && sudo apt-get install build-essential
then
exit 1
fi

if ! wget https://www.imagemagick.org/download/ImageMagick.tar.gz
then
exit 1
fi

if !  tar xvzf ImageMagick.tar.gz
then
exit 1
fi

if ! cd ImageMagick-7*
then
exit 1
fi

if ! ./configure
then
exit 1
fi

if ! make
then
exit 1
fi

if ! sudo make install && sudo ldconfig /usr/local/lib
then
exit 1
fi

if ! sudo apt install libmagick++-dev
then
exit 1
fi

if ! sudo apt-get install imagemagick-6-common imagemagick-common imagemagick-6.q16 imagemagick-common libgraphicsmagick-q16-3 libimage-magick-perl libimage-magick-q16-perl libmagic-mgc libmagic1:amd64 libmagick++-6-headers libmagick++-6.q16-7:amd64 libmagick++-6.q16-dev:amd64 libmagick++-dev libmagickcore-6-arch-config:amd64 libmagickcore-6-headers libmagickcore-6.q16-3:amd64 libmagickcore-6.q16-3-extra:amd64 libmagickwand-6-headers libmagickwand-6.q16-3:amd64 libmagickwand-6.q16-dev:amd64 libvariable-magic-perl
then
exit 1
fi
