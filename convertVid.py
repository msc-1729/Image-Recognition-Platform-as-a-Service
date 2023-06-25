from picamera import PiCamera
from time import sleep
from subprocess import call
import subprocess
import sys
import os


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# install('ffmpeg')
# install('boto3')
import json
import ffmpeg
import boto3
import _thread
import time
import subprocess
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import threading
# https://stackoverflow.com/questions/10759117/converting-jpg-images-to-png
from PIL import Image

# install('requests')
import requests

# Contants
FILE_UPLOAD_API = 'https://alcozbkh4a.execute-api.us-east-1.amazonaws.com/v1/upload'
S3_BUCKET_NAME = 'cse546project2videos'
queue_url = 'https://sqs.us-east-1.amazonaws.com/399730082620/ouputQueue'

# Initiate the camera module with pre-defined settings.
camera = PiCamera()
camera.resolution = (160, 160)
# left, top, right, bottom = 1.5*160, 160 , 2.5*160, 2*160
camera.framerate = 15
recordingTimeInsec = 3

# setting sqs
sqs = boto3.client("sqs",
	aws_access_key_id = 'AKIAV2EOFAM6NGERWENN',
    aws_secret_access_key = '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',
    region_name = 'us-east-1')

# configuring s3
s3 = boto3.client('s3', aws_access_key_id='AKIAV2EOFAM6NGERWENN',
                      aws_secret_access_key='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')

# make API call for sending images - vie API gateway
def uploadImages(location, fileName):
    with open(location, 'rb') as f:
        r = requests.post(FILE_UPLOAD_API, files={'file': f, 'fileName': fileName })
        result = r.content.decode('utf-8')
        r = json.loads(result)
        for i in r:
            for key in i:
                print(key, ":- Student Name: ", i[key]['name'] , ", id: ", i[key]['id'], ", major: ", i[key]['major'], ", year: ", i[key]['year'])

# make API call to send video files to s3
def uploadVideo(local_file, s3_file):
    try:
        s3.upload_file(local_file, S3_BUCKET_NAME, s3_file)
        print("Upload Successful")
    except FileNotFoundError:
        print("The file was not found")
    except:
        print("Credentials not available")

# polling messages 
# def poolMessagesFromQueue():
#     i = 0
#     # 2 videos in each second and 2 frames in each video
#     while i != recordingTimeInsec*2*2:
#         print("Polling messages...")
#         response = sqs.receive_message(
#             QueueUrl=queue_url,
#             MaxNumberOfMessages=10,
#             WaitTimeSeconds=1
#         )
#         if 'Messages' in response:
#             for message in response['Messages']:
#                 try:
#                     print(message['Body'])
#                     i+=1
#                 except Exception as e:
#                     print(f"exception while processing message: {repr(e)}")
#                     continue
#                 receipt_handle = message['ReceiptHandle']
#                 sqs.delete_message(
#                     QueueUrl=queue_url,
#                     ReceiptHandle=receipt_handle
#                 )

# converting and uploading for face recognition
def getFaceRecognitionResult(fileName, i):
    
    # coverting to mp4 and storing in video
    file_mp4 ="/home/pi/Desktop/CloudProject/videos/" + str(i) + ".mp4"
    file_h264 = "/home/pi/Desktop/CloudProject/" + fileName
    command = "MP4Box -add " + file_h264 + " " + file_mp4 + " -quiet"
    call([command], shell=True)
    path = "/home/pi/Desktop/CloudProject/frames/"
    # uploading mp4 video
    uploadVideo(str('/home/pi/Desktop/CloudProject/videos/'+str(i)+'.mp4'), str(i)+'.mp4')
    # converting
    os.system("ffmpeg -i " + str('/home/pi/Desktop/CloudProject/videos/'+str(i)+'.mp4') + " -r 1 " + str(path) + "image"+ str(i)+ "-%3d.jpeg -loglevel quiet")
    # upload image1
    im = Image.open(str(path) + "image"+ str(i)+ "-001.jpeg")
    # im1 = im.crop((left, top, right, bottom))
    im.save(str(path) + "image"+ str(i)+ "-001.png")
    # image 1
    start_time = time.time()
    uploadImages(str(path) + "image"+ str(i)+ "-001.png", "image"+ str(i)+ "-001.png")
    latency = time.time() - start_time
    print("Latency: {:.2f} seconds.".format(latency))

    # upload image2
    # im = Image.open(str(path) + "image"+ str(i)+ "-002.jpeg")
    # # im1 = im.crop((left, top, right, bottom))
    # im.save(str(path) + "image"+ str(i)+ "-002.png")
    # start_time = time.time()
    # uploadImages(str(path) + "image"+ str(i)+ "-002.png", "image"+ str(i)+ "-002.png")
    # latency = time.time() - start_time
    # print("Latency: {:.2f} seconds.".format(latency))
    # print("Completed and terminating thread: ", i)

    # uploading file


threads = []
camera.start_recording('1.h264')
print("recording: ", 1)
sleep(0.5)
camera.stop_recording()
threads.append(threading.Thread(target=lambda: getFaceRecognitionResult(str(1)+".h264", 1), name=str(1)))
threads[-1].start()
for i in range(2, recordingTimeInsec*2+1):
    camera.start_recording(str(i)+'.h264')
    print("recording: ", i)
    sleep(0.5)
    camera.stop_recording()
    threads.append(threading.Thread(target=lambda: getFaceRecognitionResult(str(i)+".h264", i), name=str(i)))
    threads[-1].start()
print("Completed the recording of", recordingTimeInsec, "seconds!!!")
# polling messages - ran as a separate thread
# threads.append(threading.Thread(target=lambda: poolMessagesFromQueue(), name=str(0)))
# threads[-1].start()

