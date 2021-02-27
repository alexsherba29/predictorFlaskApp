import glob
import shutil
import os
import random
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
import boto3
import logging
from botocore.exceptions import ClientError

bucket = 'stude'
class_name = ['cat', 'dog']
s3 = boto3.resource('s3')


def split_data_into_class_folders(path_to_data, class_id):
    imgs_paths = glob.glob(path_to_data + '*.jpg')

    for path in imgs_paths:

        basename = os.path.basename(path)

        if basename.startswith(str(class_id) + '_'):

            path_to_save = os.path.join(path_to_data, class_name[class_id])

            if not os.path.isdir(path_to_save):
                os.makedirs(path_to_save)

            shutil.move(path, path_to_save)


def visualize_some_images(path_to_data):
    imgs_paths = []
    labels = []

    for r, d, f in os.walk(path_to_data):
        for file in f:
            if file.endswith(".jpg"):
                imgs_paths.append(os.path.join(r, file))
                labels.append(os.path.basename(r))

    fig = plt.figure()

    for i in range(16):
        chosen_index = random.randint(0, len(imgs_paths) - 1)
        chosen_img = imgs_paths[chosen_index]
        chosen_label = labels[chosen_index]

        ax = fig.add_subplot(4, 4, i + 1)
        ax.title.set_text(chosen_label)
        ax.imshow(Image.open(chosen_img))

    fig.tight_layout(pad=0.05)
    plt.show()


def get_images_sizes(path_to_data):
    imgs_paths = []
    widths = []
    heights = []

    for r, d, f in os.walk(path_to_data):
        for file in f:
            if file.endswith(".jpg"):
                img = Image.open(os.path.join(r, file))
                widths.append(img.size[0])
                heights.append(img.size[1])
                img.close()

    mean_width = sum(widths) / len(widths)
    mean_height = sum(heights) / len(heights)
    median_width = np.median(widths)
    median_height = np.median(heights)

    return mean_width, mean_height, median_width, median_height


def download_data_to_local_directory_from_S3(photo, bucket):
    s3 = boto3.client('s3')
    s3.download_file(bucket, photo, photo)
    print("Downloand ", photo)


def detect_labels(photo, bucket):
    client = boto3.client('rekognition')

    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, MaxLabels=4,
                                    MinConfidence=90)

    print('Detected labels for ' + photo)
    print()
    for label in response['Labels']:
        if label['Name'] == 'Dog' or 'cat':
            download_data_to_local_directory_from_S3(photo, bucket)
    return len(response['Labels'])

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

if __name__ == '__main__':

    split_data_switch = False
    visualize_data_switch = False
    print_insights_switch = False
    upload_file_switch = False
    check_and_download_data_switch = False

    path_to_train_data = 'alexData/training/'
    path_to_val_data = 'alexData/validation/'
    path_to_eval_data = 'alexData/evaluation/'

    # if split_data_switch:
    #     for i in range(11):
    #         split_data_into_class_folders(path_to_train_data, i)
    #     for i in range(11):
    #         split_data_into_class_folders(path_to_val_data, i)
    #     for i in range(11):
    #         split_data_into_class_folders(path_to_eval_data, i)

    if visualize_data_switch:
        visualize_some_images(path_to_train_data)

    if print_insights_switch:
        mean_width, mean_height, median_width, median_height = get_images_sizes(path_to_train_data)

        print("mean width = {mean_width}")
        print("mean height = {mean_height}")
        print("median width = {median_width}")
        print("median height = {median_height}")

    if upload_file_switch:
        upload_dir_path = 'alexData/training/'
        for className in class_name:
            entries = os.listdir(upload_dir_path + className)
            for entry in sorted(entries):
                upload_file(upload_dir_path + className + '/' + entry, bucket, 'alexData/' + className + '/' + entry)
                print(entry)
            print("Done")

    if check_and_download_data_switch:
        download_dir_path = 'testDownloandDir'
        filename = 'alexData/'
        my_bucket = s3.Bucket(bucket)
        for my_bucket_object in my_bucket.objects.filter(Prefix='alexData/'):
            if my_bucket_object.key.endswith(".jpg"):
                # print(my_bucket_object.key)
                label_count = detect_labels(my_bucket_object.key, bucket)
                print("Labels detected: " + str(label_count))
                download_data_to_local_directory_from_S3(my_bucket_object, bucket)
