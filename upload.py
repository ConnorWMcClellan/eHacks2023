import boto3
import os

s3 = boto3.resource("s3")
bucket = s3.Bucket('flyinlions')
collection_id = 'collection-id'

directory = 'images'

for filename in os.scandir(directory):
    f = os.path.join(directory, filename)
    filename = f.split('/')
    print(filename[2])
    bucket.upload_file("images" + '/' + filename[2], filename[2])
    os.remove("images" + '/' + filename[2])
