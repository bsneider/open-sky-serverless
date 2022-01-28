import boto3
from botocore.exceptions import NoCredentialsError
from botocore.vendored import requests

# Psuedo code
# Requests, download the file
# upload file to s3
remote_url = "https://zenodo.org/record/5377831/files/flightlist_20190101_20190131.csv.gz?download=1"
bucket_name = "${bucket_name}"
file_name = "${file_name}"
#  Source https: // erangad.medium.com/upload-a-remote-image-to-s3-without-saving-it-first-with-python-def9c6ee1140
# https://stackoverflow.com/questions/40741282/cannot-use-requests-module-on-aws-lambda


def lambda_handler(event, context):
    # body = json.loads(event["body"])
    # url_of_the_file_to_be_uploaded = body['url']
    # file_name = url_of_the_file_to_be_uploaded.split("/")[-1].split("?")[0]
    # bucket_name = body['bucket-name']
    return upload_file(remote_url,
                       bucket_name, file_name)


def upload_file(remote_url, bucket, file_name):
    s3 = boto3.client('s3')
    try:
        response = requests.get(remote_url, stream=True).raw
        s3.upload_fileobj(response, bucket, file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
