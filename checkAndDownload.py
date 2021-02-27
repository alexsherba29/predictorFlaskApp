import os

import boto3
import logging
from botocore.exceptions import ClientError

LABEL = "Dog"

def downloandFromS3(photo, bucket):
    s3 = boto3.client('s3')
    s3.download_file(bucket, photo, photo)


def detect_labels(photo, bucket):
    client = boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, MaxLabels=4, MinConfidence=90)

    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        if label['Name'] == 'Dog':
            # print("Label: " + label['Name'])
            # print("Confidence: " + str(label['Confidence']))
            # print("Instances:")
            # for instance in label['Instances']:
            #     print("  Bounding box")
            #     print("    Top: " + str(instance['BoundingBox']['Top']))
            #     print("    Left: " + str(instance['BoundingBox']['Left']))
            #     print("    Width: " + str(instance['BoundingBox']['Width']))
            #     print("    Height: " + str(instance['BoundingBox']['Height']))
            #     print("  Confidence: " + str(instance['Confidence']))
            #     print()
            #
            # print("Parents:")
            # for parent in label['Parents']:
            #     print("   " + parent['Name'])
            # print("----------")
            # print()
            downloandFromS3(photo, bucket)
    return len(response['Labels'])


def main():
    dir_path = 'dataset/dog/'
    bucket = 'stude'
    filename = 'alexData/dog/'
    entries = os.listdir(dir_path)
    # upload files from folder
    # for entry in sorted(entries):
    #     upload_file(dir_path + entry, bucket, 'alexData/{}'.format(entry))
        # print(filename)
        # print(entry)
    # send images to Rekognition
    for entry in sorted(entries):
        label_count = detect_labels(filename + '{}'.format(entry), bucket)
        print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
