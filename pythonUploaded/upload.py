import boto3
import os

session = boto3.Session(
    aws_access_key_id='AKIASZO4MXVBEKXQVIDE',
    aws_secret_access_key='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',
)

s3 = session.resource("s3")
bucket = s3.Bucket('flyinlions')
collection_id = 'collection-id'




directory = 'images'

while True:
    try:
        for filename in os.scandir(directory):
            f = os.path.join(directory, filename)
            filename = f.split('\\')
            bucket.upload_file('images' + '\\' + filename[2], filename[2])
            os.remove('images' + '\\' + filename[2])
    except:
        print("directory empty")