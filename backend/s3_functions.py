import logging
import boto3
import hashlib
import time


def upload_file(user_id, file_name, file_video, bucket, prefix=None):
    """Uploads a file to s3, generating a unique id for the file

    Parameters
    ----------
    user_id : str
        id of the user uploading the file
    file_name : str
        name of file
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
        str.encode(user_id + file_name + str(time.time()))
    ).hexdigest()
    bucket_filename = '{}/{}.mp4'.format(prefix, file_id)

    s3_client = boto3.client('s3', region_name='us-east-1')
    try:
        s3_client.upload_fileobj(file_video, bucket, bucket_filename)
        return file_id
    except s3_client.exceptions.ClientError as e:
        logging.error(e)
        return False
