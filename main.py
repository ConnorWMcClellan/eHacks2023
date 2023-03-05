import boto3  # pip install boto3
import re
from comm import *

s3 = boto3.resource("s3")
bucket = s3.Bucket('flyinlions')

# bucket.upload_file("images/img.jpg","tonystark")
# bucket.upload_file("images/img_2.png", "cap")


def create_collection(collection_id):
    session = boto3.Session(profile_name='CWM5100')
    client = session.client('rekognition')

    # Create a collection
    print('Creating collection:' + collection_id)
    response = client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

def list_faces_in_collection(collection_id):
    maxResults = 2
    faces_count = 0
    tokens = True

    session = boto3.Session(profile_name='CWM5100')
    client = session.client('rekognition')
    response = client.list_faces(CollectionId=collection_id,
                                 MaxResults=maxResults)

    print('Faces in collection ' + collection_id)

    while tokens:

        faces = response['Faces']

        for face in faces:
            print(face)
            faces_count += 1
        if 'NextToken' in response:
            nextToken = response['NextToken']
            response = client.list_faces(CollectionId=collection_id,
                                         NextToken=nextToken, MaxResults=maxResults)
        else:
            tokens = False
    return faces_count

def add_faces_to_collection(bucket, photo, collection_id):

    session = boto3.Session(profile_name='CWM5100')
    client = session.client('rekognition')

    response = client.index_faces(CollectionId=collection_id,
                                  Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                  ExternalImageId=photo,
                                  MaxFaces=1,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['ALL'])

    print('Results for ' + photo)
    print('Faces indexed:')
    for faceRecord in response['FaceRecords']:
        print('  Face ID: ' + faceRecord['Face']['FaceId'])
        print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])

def iterate_bucket_items(bucket):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=bucket)
    collection = []
    for page in page_iterator:
        if page['KeyCount'] > 0:
            for item in page['Contents']:
                yield item


def main():
    collection_id = 'collection-id'
    s3 = boto3.resource("s3")
    employeeBucket = 'flyinlions'
    collection_id = 'Employees'

    #indexed_faces_count = add_faces_to_collection(bucket, photo, collection_id)
    threshold = 70
    maxFaces = 2
    client = boto3.client('rekognition')

    collection = []

    for i in iterate_bucket_items(bucket='flyinlions'):
        #collection.append(i['Key'])

    #for i in collection:
        response = client.search_faces_by_image(CollectionId=collection_id,
                                                Image={'S3Object': {'Bucket': employeeBucket, 'Name': i['Key']}},
                                                FaceMatchThreshold=threshold,
                                                MaxFaces=maxFaces)

        faceMatches = response['FaceMatches']
        print('Matching faces')
        match = 0

        for match in faceMatches:
            img = match['Face']['ExternalImageId']
            name = img.split('.')
            print(name[0])
            print('FaceId:' + match['Face']['FaceId'])
            print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            if match['Similarity'] >= 70:
                match = 1
                break
        if match == 1:
            print('Found  :' + i['Key'])
            splitName = re.sub(r"([A-Z])", r" \1", name[0]).split(None, 1)
            print(splitName[0])
            print(splitName[1])
            s3.Object('flyinlions', i['Key']).delete()
            #addRecord(splitName[0], splitName[1])
        else:
            print('No match found  :' + i['Key'])


if __name__ == "__main__":
    main()
