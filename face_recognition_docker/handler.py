from http import client
import os
import boto3
from torch import bucketize
from eval_face_recognition import eval_faceRecognition

"""session = boto3.Session(
	aws_access_key_id = 'AKIAV2EOFAM6NGERWENN ',
    aws_secret_access_key = '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 ',
    region_name = 'us-east-1'
	)"""
s3 = boto3.client(
	's3',
	aws_access_key_id = 'AKIAV2EOFAM6NGERWENN',
    aws_secret_access_key = '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',
    region_name = 'us-east-1'
	)

def face_recognition_handler(event, context):
	bucketName = event['bucketName']
	keyName = event['keyName']
	response = s3.get_object(Bucket=bucketName, Key=keyName)
	emailcontent = response['Body'].read()
	# print(emailcontent)
	with open('../../tmp/'+keyName, 'wb') as f: 
		f.write(emailcontent)
	print("writing completed!")
	result =  eval_faceRecognition('../../tmp/'+keyName)
	return result

# face_recognition_handler({"bucketName":"cse546project2videos", "keyName":"hello.png"},"")
 