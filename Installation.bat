@echo off
Installing the required libraries for using the "Image recognition Platform as a Service using AWS"
cd \
pip install boto3
pip install dlib
pip install numpy
pip install face_recognition
pip install opencv-python
pip install ffmpeg
pip install botocore
pip install awslambdaric

pause
exit