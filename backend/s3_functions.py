import logging
import boto3
import hashlib
import time
from botocore.exceptions import ClientError


def upload_file(file_path, bucket):

    file_id = hashlib.sha1(str.encode(file_path)).hexdigest()
    bucket_filename = '{}.mp4'.format(file_id)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, bucket_filename)
        return bucket_filename
    except ClientError as e:
        logging.error(e)
        return False
