import json

# Psuedo code
# Requests, download the file
# upload file to s3
"https://zenodo.org/record/5377831/files/flightlist_20190101_20190131.csv.gz?download=1"


import mimetypes

# Source https: // erangad.medium.com/upload-a-remote-image-to-s3-without-saving-it-first-with-python-def9c6ee1140
import boto3
from botocore.exceptions import NoCredentialsError
# https://stackoverflow.com/questions/40741282/cannot-use-requests-module-on-aws-lambda
from botocore.vendored import requests

ACCESS_KEY_ID = '*************'
SECRET_ACCESS_KEY = '********************************'


def lambda_handler(event, context):
    body = json.loads(event["body"])
    url_of_the_file_to_be_uploaded = body['url']
    file_name = url_of_the_file_to_be_uploaded.split("/")[-1].split("?")[0]
    bucket_name = body['bucket-name']
    return upload_file(url_of_the_file_to_be_uploaded,
                       bucket_name, file_name)


def upload_file(remote_url, bucket, file_name):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID,
                      aws_secret_access_key=SECRET_ACCESS_KEY)
    try:
        response = requests.get(remote_url, stream=True).raw
        # content_type = response.headers['content-type']
        # extension = mimetypes.guess_extension(content_type)
        s3.upload_fileobj(response, bucket, file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
