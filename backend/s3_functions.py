import logging
import boto3
import hashlib
import time
from botocore.exceptions import ClientError


def upload_file(user_id, file_path, bucket, prefix=None):
    """Uploads a file to s3, generating a unique id for the file

    Parameters
    ----------
    user_id : str
        id of the user uploading the file
    file_path : str
        path to the file
    bucket : str
        name of the bucket
    prefix : str, optional
        file prefix (sub folders in the bucket), by default None

    Returns
    -------
    str
        generated id of the file
    """
    if prefix is None:
        prefix = ''
    file_id = hashlib.sha1(
        str.encode(user_id + file_path + str(time.time()))
    ).hexdigest()
    bucket_filename = '{}/{}.mp4'.format(prefix, file_id)

    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_path, bucket, bucket_filename)
        return file_id
    except ClientError as e:
        logging.error(e)
        return False
