import json
import base64
import boto3
import email

BUCKET_NAME = 'cse546project2videos'

def lambda_handler(event, context):
    
    print(event)
    
    s3 = boto3.client("s3")
    
    lambdaTrigger = boto3.client("lambda")

    # decoding form-data into bytes
    post_data = base64.b64decode(event["body"])
    # fetching content-type
    # print(post_data)
    try:
        content_type = event["headers"]["Content-Type"]
    except:
        content_type = event["headers"]["content-type"]
    # concate Content-Type: with content_type from event
    ct = "Content-Type: " + content_type + "\n"

    # parsing message from bytes
    msg = email.message_from_bytes(ct.encode() + post_data)

    # checking if the message is multipart
    # print("Multipart check : ", msg.is_multipart())

    # if message is multipart
    if msg.is_multipart():
        try:
            multipart_content = {}
            # retrieving form-data
            for part in msg.get_payload():
                # checking if filename exist as a part of content-disposition header
                if part.get_filename():
                    # fetching the filename
                    file_name = part.get_filename()
                multipart_content[
                    part.get_param("name", header="content-disposition")
                ] = part.get_payload(decode=True)
    
            # filename from form-data
            file_name = multipart_content["fileName"]
            
            # u uploading file to S3
            s3_upload = s3.put_object(
                Bucket=BUCKET_NAME, Key=str(file_name)[2:-1] , Body=multipart_content["file"]
            )
        
            print("File uploaed successfully")
            
            # call facerecognition lambda and get result
            faceRecognitionBody = {
              "bucketName": BUCKET_NAME,
              "keyName": str(file_name)[2:-1]
            }
            
            print(faceRecognitionBody)
            
            fR_result = lambdaTrigger.invoke(
                FunctionName = 'arn:aws:lambda:us-east-1:399730082620:function:Face_Recognition',
                InvocationType = 'RequestResponse',
                Payload = json.dumps(faceRecognitionBody)
            )
            
            # (hello.png, jayanth_kumar_tumuluri)
            # print(fR_result['Payload'].read())
            payload = json.loads(fR_result['Payload'].read())
            print(payload)
            studentName = str(payload.split(",")[-1][:-1])
            
            print(studentName)
            # # temp
            dynamoSearch = { 'name': studentName, 'requestKey': str(payload.split(",")[0][1:]) }
            
            dynamoResp = lambdaTrigger.invoke(
                FunctionName = 'arn:aws:lambda:us-east-1:399730082620:function:getResultsFromDynamoDB',
                InvocationType = 'RequestResponse',
                Payload = json.dumps(dynamoSearch)
                )
                
            print("Dynamo Response: " , dynamoResp)
            payload = json.loads(dynamoResp['Payload'].read())
            print(payload)
            return {"statusCode": 200, "body": json.dumps(payload)}
            
        except:
            return {"statusCode": 500, "body": json.dumps("Upload failed or Internal Server Error!")}
    else:
        # on upload failure
        return {"statusCode": 500, "body": json.dumps("Upload failed or Internal Server Error!!!")}