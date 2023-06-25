# # Importing Image class from PIL module
# from PIL import Image
 
# # Opens a image in RGB mode
# im = Image.open("image1-002.png")
 
# # Size of the image in pixels (size of original image)
# # (This is not mandatory)
# width, height = im.size
 
# left, top, right, bottom = 2.7*160, 1.9*160 , 3.7*160, 2.9*160
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((left, top, right, bottom))

# im1.save("image1.png")
import boto3

sqs = boto3.client("sqs",
	aws_access_key_id = 'AKIAV2EOFAM6NGERWENN',
    aws_secret_access_key = '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',
    region_name = 'us-east-1')

queue_url = 'https://sqs.us-east-1.amazonaws.com/399730082620/ouputQueue'
while True:
    print("Polling messages...")
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
        WaitTimeSeconds=1
    )
    print(type(response), len(response), response.keys())
    if 'Messages' in response:
        for message in response['Messages']:
            try:
                print(message['Body'])
            except Exception as e:
                print(f"exception while processing message: {repr(e)}")
                continue
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )