## Setup
After using terraform to create the VPC instance, you will need to copy the `ffmpeg-python-setup.sh` script to set ffmpeg tool up.

```bash
scp -i ~/.ssh/video-messaging-processing-kp.pem infrastructure/ffmpeg-python-setup.sh ec2-user@3.249.200.229:~/
```

Then ssh in the instance and run the script.

```bash
ssh -i ~/.ssh/video-messaging-processing-kp.pem ec2-user@3.249.200.229
sudo su
./ffmpeg-python-setup.sh
```

### Adding video processing script

```bash
 scp -i ~/.ssh/video-messaging-processing-kp.pem videoProcessor.py ec2-user@3.249.200.229:~/
```

I had to export the below credentials - need to add them into param store and include them in the setup script

```bash
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=k
export AWS_REGION=eu-west-1
export AWS_ACCOUNT_ID=
```

## Running Listener

A background task is needed so that when you quit out the vm - the listener doesn't stop.

Environment variables need to be set in screen.

```bash
screen (-r)
python3 videoProcessor.py
```

## Test Message
```json
{
    "Message": "{\"campaignId\":\"jakeid\",\"videoOrder\":[\"https:\/\/video-messaging-library-videos.s3.eu-west-2.amazonaws.com\/Video1.mp4\",\"https:\/\/video-messaging-library-videos.s3.eu-west-2.amazonaws.com\/Video9.mp4\",\"https:\/\/video-messaging-library-videos.s3.eu-west-2.amazonaws.com\/Video10.mp4\"],\"email\":\"jakeowen.ex@gmail.com\",\"videoName\":\"here\",\"introductionPictureUrl\":\"here\",\"traceId\":\"here\"}"
}
```