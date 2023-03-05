import boto3
import os

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

def create_collection(collection_id):
    session = boto3.Session(profile_name='CWM5100')
    client = session.client('rekognition')

    # Create a collection
    print('Creating collection:' + collection_id)
    response = client.create_collection(CollectionId=collection_id)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')

def main():

    #create_collection('Employees')
    s3 = boto3.resource("s3")
    bucket = s3.Bucket('employees-ats')
    collection_id = 'Employees'
    directory = 'images'
    name = input("Enter Employee Name: ")

    #print(list_faces_in_collection('Employees'))
    for filename in os.scandir(directory):
        f = os.path.join(directory, filename)
        filename = f.split('/')
        photo = name.split('.')
        #os.remove("images" + '/' + filename[2])
        bucket.upload_file("images" + '/' + filename[2], filename[2])
        bucket2 = 'employees-ats'
        if name == photo[0]:
            add_faces_to_collection(bucket2, filename[2], collection_id)
            print("Employee Added")
            os.remove("images" + '/' + filename[2])


if __name__ == "__main__":
    main()