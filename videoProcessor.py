import logging
import sys
logger = logging.getLogger('sqs_listener')
logger.setLevel(logging.INFO)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)

formatstr = '[%(asctime)s - %(name)s - %(levelname)s]  %(message)s'
formatter = logging.Formatter(formatstr)

sh.setFormatter(formatter)
logger.addHandler(sh)
from sqs_listener import SqsListener
import boto3
import json
import os
import pathlib
import glob
path = pathlib.Path().absolute()

class VideoProcessor(SqsListener):
    def handle_message(self, body, attributes, messages_attributes):
        s3_client = boto3.client('s3')
        message = json.loads(body["Message"])

        campaignId = message["campaignId"]
        clientId = message["clientId"]
        userId = message["userId"]
        videos = message["videoOrder"]
        print("Processing CampaignId: {0} ...".format(campaignId))

        print("Processing videos to standardise scale and video/audio encoding...")
        os.system("ffmpeg -protocol_whitelist http,https,file,crypto,data,tls,tcp -i {0} -sn -vf scale=1920:1080,setsar=1 "
                  "-r 30 -vcodec h264 -acodec aac -ar 48000 output-{1}"
                  .format(videos[0], self.getUnprocessedVideoKey(videos[0])))
        
        for video in videos[1:]:
            os.system("ffmpeg -protocol_whitelist http,https,file,crypto,data,tls,tcp -i {0} -sn -vf scale=1920:1080 "
                      "-vcodec h264 -acodec aac -ar 48000 output-{1}"
                      .format(video, self.getUnprocessedVideoKey(video)))
        
        newFiles = glob.glob('output-*')
        newFiles.sort(key=os.path.getmtime)
        print("Process following files into .ts format {0}".format(str(newFiles)))
        concatString = ''
        for file in newFiles:
            tempFile = "temp-{0}.ts".format(file)
            os.system("ffmpeg -i {0} -c copy -bsf:v h264_mp4toannexb -f mpegts {1}"
                      .format(file, tempFile))
            concatString += tempFile + "|"
        concatString = concatString[:-1]
        
        print("Creating final video...")
        key = "{0}-{1}-{2}-final.mp4".format(userId, campaignId, clientId)
        os.system('ffmpeg -i "concat:{0}" -c:v copy -bsf:a aac_adtstoasc {1}'
                  .format(concatString, key))
        
        print("Uploading processed video {0} to s3...".format(key))
        
        self.uploadToProcessedBucket(s3_client, userId, campaignId, clientId)
        
        print("Removing all created files from local dir...")
        files = glob.glob('*.mp4*')
        for file in files:
            os.system("rm {0}".format(file))

        self.publishToSNS(userId, campaignId, clientId)
        print("Done!")

    def getUnprocessedVideoKey(self, url):
        end = url.find(".com/")
        return (url[end + 5:len(url)]).replace("/", "-")

    def uploadToProcessedBucket(self, s3_client, userId, campaignId, clientId):
        s3_client.upload_file("{0}-{1}-{2}-final.mp4".format(userId, campaignId, clientId),
                              "messaging-processed-videos",
                              "{0}/{1}/{2}/final.mp4".format(userId, campaignId, clientId),
                              ExtraArgs={'ACL': 'public-read', 'ContentType': 'video/mp4'})

    def deleteFromBucket(self, s3_client, bucket, key):
        s3_client.delete_object(Bucket=bucket, Key=key)

    def publishToSNS(self, userId, campaignId, clientId):
        sns_client = boto3.client('sns', region_name='eu-west-1')
        snsMessage = {
            "clientId": clientId,
            "userId": userId,
            "campaignId": campaignId
        }
        sns_client.publish(
            TopicArn='arn:aws:sns:eu-west-1:686976128650:video-messaging-enricher-topic',
            Message=json.dumps(snsMessage)
        )


listener = VideoProcessor('video-messaging-processor-queue', interval=1, region_name='eu-west-1', force_delete=True)
print("Listening...")
listener.listen()
