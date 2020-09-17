cd /usr/local/bin
mkdir ffmpeg && cd ffmpeg
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz
tar -xf ffmpeg-release-arm64-static.tar.xz
cd ffmpeg-4.3-arm64-static/
./ffmpeg version
cp -a /usr/local/bin/ffmpeg/ffmpeg-4.3-arm64-static/ . /usr/local/bin/ffmpeg/
ln -s /usr/local/bin/ffmpeg/ffmpeg /usr/bin/ffmpeg
ffmpeg

sudo amazon-linux-extras install python3.8
sudo yum update
sudo easy_install pip
sudo pip3 install pySqsListener
sudo pip3 install boto3
sudo pip3 install pathlib

export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_REGION=eu-west-1
export AWS_ACCOUNT_ID=
