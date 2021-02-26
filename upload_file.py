import os

import boto3
import logging
from botocore.exceptions import ClientError


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def main():
    dir_path = 'dataset/dog/'
    bucket = 'stude'
    filename = 'alexData/dog/'
    entries = os.listdir(dir_path)
    # upload files from folder
    for entry in sorted(entries):
        upload_file(dir_path + entry, bucket, 'alexData/{}'.format(entry))
        # print(filename)
        # print(entry)
    print("Done")

if __name__ == "__main__":
    main()