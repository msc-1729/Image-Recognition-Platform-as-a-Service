<h2 align="center"> Image Recognition - Platform as a Service </h2>

# Introduction

The main aim of the project is to create a distributed application to conduct real-time face recognition 
on videos captured by edge devices in real-time. We have utilized Raspberry Pi for the IoT part which 
includes a Python script to record the videos and AWS Lambda for the Platform as a Service part which 
includes the scripts to extract the frames from the raspberry pi, perform face recognition and 
send the results from DynamoDB to Raspberry Pi. We have also used the Amazon Elastic container registry 
to store the container image. Lambda is the most extensively used Function as a service iteration of the 
PaaS. Raspberry Pi is by far the most famous IoT development platform.

# Architecture
A video is recorded in the raspberry pi continuously for around 5 minutes. A multi-threaded python 
the script inside the raspberry pi is written where these threads perform the following tasks:

● Uploads the frames from the video to the input S3 bucket </br>
● Continuously records the video for 5 minutes. 

The frames from the recorded video are uploaded to the S3 bucket via the API Gateway. In the AWS Lambda, we created two functions one to perform the face recognition task on the container image and the other to get the results from DynamoDB and send those results to the raspberry pi. The upload_videos lambda is triggered by the API Gateway whenever it receives the frames from the raspberry pi. This lambda function will extract the data received from the API Gateway as multipart form data and upload this data  to the S3 so that the frames are backed up. A container image is created in the ECR and fetched by the Face_recognition Lambda function for the face recognition task. The upload_videos lambda function will invoke the face recognition lambda function and send the input frames from the S3 bucket. Once the recognition is done this function invokes the DynamoDB to search the details of the person which the face recognition function recognizes and then sends the dynamo search results back to the raspberry pi via the API Gateway. 

<img src = "https://github.com/msc-1729/Image-Recognition-Platform-as-a-Service/blob/main/assets/Architecture.png"/>

# Concurrency and Latency

* Concurrency: Concurrency is achieved using multi-threading. A more detailed understanding can be found in the App Tier of the code section.
* Latency: Latency can be reduced by performing the frame extraction process inside the raspberry pi instead of doing it in a separate lambda function.

# Testing and Evaluation
We tested our code from point to point and also tested it extensively after the final integration. 
We have checked whether the videos are being sent to the S3 from the Pi using lambda. We have also tested 
to make sure that the facial recognition lambda functions are being created correctly. According to our 
methodology, frames will be uploaded to S3 every 0.5 seconds, so we have also checked whether this 
functionality is working as intended and storing the frames in S3 from the Pi. We have also made sure that 
the information is stored correctly in DynamoDB. Before using the model, we trained it with the 
images of the teammates and achieved a validation accuracy of 89 percent. We then tested the 
application with the input video being one with our faces and tested the accuracy. We have also fine-tuned the neural network model by using various optimizers and different batch sizes. At last, we also tested 
and made sure that the end-to-end latency is not high. 

# Code
The whole project into different tiers making it a multi-tiered architecture. The two levels of this architecture can be explained as follows:
  * App Tier:  The raspberry pi python program which is running on the raspberry pi operating system.
  * Web Tier:  This is the AWS itself and it includes and utilizes various services like API Gateway, 
               S3, Lambdas and DynamoDB.
### App Tier: 

The Python script inside the Raspberry Pi performs the following functionalities:
It continuously records video for the given number of seconds (5*60) which is 5 minutes according to the 
problem statement and for each 0.5-second duration a video is generated and stored in a specific location. 

Each video is now passed on to a method (getFaceRecognitionResult) which is run as a thread. 
Example: We will get a total of 5*60*2 videos from the 5 minutes and each 0.5-second video is passed on 
to a thread. So, the total number of threads that get generated and executed is 5*60*2. These are executed independently using multi-threading. 
getFaceRecognitionResult performs the following operations:
1. Extract frames from the given video after converting it into mp4 using the MP4box library.
2. Upload the video into the S3 bucket.
3. Send the image for a face recognition task. The image will also be uploaded into S3 via the lambda function before performing face recognition.

### Web Tier:
As said previously, It utilizes some AWS services to cater the scalable and low latent face recognition 
service. 
We utilized the API Gateway to expose an API to App Tier and serve it. And this API internally calls the 
UploadVideos lambda function. This lambda function performs the necessary operations and returns the 
response to the Raspberry Pi.

### Lambda Fucntions:

  * ### UploadVideos Functionalities:
    * Extract the image file and fileName from the multipart form data.
    * Put the image file into the S3 bucket. And calls the lambda Face_Recognition by passing the file key 
      name in the S3 bucket as a parameter
    * Face_Recognition performs a face recognition task and returns the result back say fr.
    * Now the response fr is passed into another lambda function getResultsFromDynamoDB as 
      a parameter.
    * getResultsFromDynamoDB returns the complete student information by performing the scan 
      operation using the fr (which is the student name).
    * Result from the getResultsFromDynamoDB is returned back to the Raspberry Pi as a response.
  * ### Face_Recognition functionalities:
    * A docker image is tagged to the lambda from the ECR repository to perform face recognition.
    * This image contains the code snippets and the trained face recognition model.
    * Perform a face recognition task and return the result.
  * ### getResultsFromDynamoDB functionalities:
    * It gets the student's name as an input parameter.
    * Do a scan operation using the student's name and get the complete student information and return it.

 
 # Steps to Execute the Code
 * Install all the required libraries for creating the distributed application by running the bat file provided
 * Connect to the raspberry pi using any of the connection methods (SSH/ HDMI/ Ethernet cable).
 * Run the convertVid.py script inside the raspberry pi.
 * Once the script execution is completed the results are seen in the console.

# ImageRecognitionPaaS
* ["sh","/entry.sh"]
* pip3 install torch==1.11.0+cpu torchvision==0.11.3+cpu torchaudio==1.10.2+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
