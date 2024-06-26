"""
S3 utility functions
=======================
Curation of utility functions required for accessing and performing operations in AWS S3 (Simple Storage Services).
"""
import json
import logging
import os
from pathlib import Path

import boto3

# Initialising the logger
LOGGER = logging.getLogger(__name__)


def connect_s3(aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None):
    """
    Module to establish connection with s3. If the credentials and access tokens are passed then it considers the
    connection to be local and connects to s3, otherwise it obtains the connection information via IAM role policy
    directly.

    :param aws_access_key_id: AWS access key ID. Default is `None`
    :type aws_access_key_id: str
    :param aws_secret_access_key: AWS secret access key. Default is `None`
    :type aws_secret_access_key: str
    :param aws_session_token: AWS session token. Default is `None`
    :type aws_session_token: str
    :return: pointer to AWS
    :rtype: <class botocore.client.S3>
    """

    if aws_access_key_id and aws_secret_access_key and aws_session_token:
        LOGGER.debug("AWS access credentials passed exclusively, establishing connection.")
        s3_client = boto3.client('s3',
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key,
                                 aws_session_token=aws_session_token)

    else:
        LOGGER.debug("AWS access credentials not passed explicitly, accessing based on IAM role privilages.")
        s3_client = boto3.client('s3')

    return s3_client


def put_s3_object(s3_client, bucket, file_name, dict_obj_to_upload):
    """
    Module to upload the file from **memory** to s3. Instead of pushing an already existing JSON to S3, this exports
    `dict` object to bucket.

    :param s3_client: boto3 client pointer
    :type s3_client: <class botocore.client.S3>
    :param bucket: name of the bucket where object will be uploaded
    :type bucket: str
    :param file_name: name of object in bucket. If a dir name is required then this should be "<dir_name>/<filename>"
    :type file_name: str
    :param dict_obj_to_upload: dictionary object for the upload to bucket
    :type dict_obj_to_upload: dict
    :return: nothing
    :rtype: None
    """

    json_string = json.dumps(dict_obj_to_upload)
    bytes_data = json_string.encode('utf-8')

    response = s3_client.put_object(
        Bucket=bucket,
        Key=file_name,
        Body=bytes_data
    )
    LOGGER.debug(f"{file_name} uploaded to {bucket} bucket.")


def upload_objects(file_path, s3_client, export_bucket, upload_dir_name):
    """
    Module to upload the files (objects) from system to s3.

    :param s3_client: boto3 client pointer
    :type s3_client: <class botocore.client.S3>
    :param file_path: file path containing the file name as well
    :type file_path: str
    :param export_bucket: name of bucket where the export will be made
    :type export_bucket: str
    :param upload_dir_name: name of directory within which the data will be pushed. Can be empty string (""). \
    This is required when you need to push the data other than bucket root path.
    :type upload_dir_name: str
    """

    file_basename = file_path.split('/')[-1]
    _upload_path = f"{upload_dir_name}/{file_basename}" if upload_dir_name else file_basename

    s3_client.upload_file(file_path,
                          export_bucket,
                          _upload_path
                          )


def download_object(s3_client, file_name, s3_bucket, download_dir=None):
    """
    Module to download the S3 objects in `download_dir`.
    If `file_name` contains the s3 directory information then it is trimmed and only filename is retained.

    :param file_name: name of the file to download. Name can also contain the dirname where the file resides within s3.
    :type file_name: str
    :param s3_client: boto3 client pointer
    :type s3_client: <class botocore.client.S3>
    :param s3_bucket: name of s3 bucket
    :type s3_bucket: str
    :param download_dir: path where the file will be downloaded. It is optional. If not provided, downloads the file in current dir. Default is `None`.
    :type download_dir: str
    :return: composed download path where file got downloaded (download path + filename).
    :rtype: str
    """

    # checking whether file_name contains the subdir. If so, the dirname is trimmed off
    _dir_info = file_name.split("/")
    _f_name = os.path.basename(file_name) if len(_dir_info) > 1 else file_name

    download_path = Path(download_dir) / _f_name if download_dir else _f_name

    s3_client.download_file(
        s3_bucket,
        file_name,
        str(download_path)
    )
    LOGGER.debug(f"Downloaded {file_name} to {download_path}")
    return download_path


def copy_s3_object(s3_client, from_bucket, to_bucket, file_name):
    """
    Module to copy the object from one S3 bucket to another.
    Ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/copy_object.html

    :param s3_client: boto3 client pointer
    :type s3_client: <class botocore.client.S3>
    :param from_bucket: s3 bucket *from* which the file has to be copied (source bucket)
    :type from_bucket: str
    :param to_bucket: s3 bucket *to* which the file will be copied (destination bucket)
    :type to_bucket: str
    :param file_name: name of file that need to be copied
    :type file_name: str
    :return: nothing
    :rtype: None
    """
    # todo: add an exception for copy failure
    # todo: add an exception when the file is not found in the source bucket
    # todo: add case when file is inside a directory OR to be copied inside a directory. Add PREFIX component
    s3_client.copy_object(
        Bucket=to_bucket,
        CopySource={'Bucket': from_bucket, 'Key': file_name},
        Key=file_name
    )
    LOGGER.info(f"{file_name} file has been copied successfully from {from_bucket} to {to_bucket} s3 bucket")


def move_s3_object(s3_client, from_bucket, to_bucket, file_name):
    """
    Module to move the object from one S3 bucket to another. This is similar to copy but there is an addition of
    delete operation that removes the file from source bucket.

    :param s3_client: boto3 client pointer
    :type s3_client: <class botocore.client.S3>
    :param from_bucket: s3 bucket *from* which the file has to be copied (source bucket)
    :type from_bucket: str
    :param to_bucket: s3 bucket *to* which the file will be copied (destination bucket)
    :type to_bucket: str
    :param file_name: name of file that need to be copied
    :type file_name: str
    :return: nothing
    :rtype: None
    """
    # todo: add an exception for copy failure
    # todo: add an exception when the file is not found in the source bucket
    # todo: add case when file is inside a directory OR to be copied inside a directory. Add PREFIX component
    s3_client.copy_object(
        Bucket=to_bucket,
        CopySource={'Bucket': from_bucket, 'Key': file_name},
        Key=file_name
    )
    s3_client.delete_object(Bucket=from_bucket, Key=file_name)
    LOGGER.info(f"{file_name} file has been moved successfully from {from_bucket} to {to_bucket} s3 bucket")


def delete_s3_object(s3_client, bucket, file_name):
    """
    Delete an object from S3 bucket.

    :param s3_client: boto3 client pointer
    :type s3_client: <class botocore.client.S3>
    :param bucket: name of the bucket from where the object has to be deleted.
    :type bucket: str
    :param file_name: name of the file/ object to be deleted
    :type file_name: str
    :return: nothing
    :rtype: None
    """

    response = s3_client.delete_object(
        Bucket=bucket,
        Key=file_name,
    )
    LOGGER.debug(f"{file_name} has been deleted from {bucket} bucket.")


def list_s3_files(s3_client, bucket_name, content_dir_name, list_only_extn=".json"):
    """
    List all the files in given s3 location.

    :param s3_client: boto3 s3 pointer
    :type s3_client: <class botocore.client.S3>
    :param bucket_name: name of s3 bucket
    :type bucket_name: str
    :param content_dir_name: directory within s3 bucket from where the data will be listed. If empty string is
    passed it lists all the `.json` files from the bucket.
    :type content_dir_name: str
    :param list_only_extn: Only list the files of given extension. Provide an extn with a period ex ".csv", ".json" etc. Can be empty str ("") if list of all the files is required.
    :type list_only_extn: str
    :return: list of all files
    :rtype: list
    """
    # todo: if the prefix is provided, it also checks the content of nested dirs present within prefix. Catch the issue.
    if content_dir_name:  # if objects within a specific directory are to be listed instead of entire bucket
        try:
            objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=f"{content_dir_name}/")
            all_files = [obj['Key'] for obj in objects['Contents']]
        except KeyError:
            raise KeyError(f"{content_dir_name} not found in {bucket_name} bucket.")

    else:
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        try:
            all_files = [obj['Key'] for obj in objects['Contents']]
        except KeyError:  # if the bucket exists but empty {KeyError: 'Contents'} will be raised
            LOGGER.warning(f"Bucket exists but found to be empty")
            all_files = objects.get('Contents', [])

    # Ensuring that only files with intended extensions gets listed
    if list_only_extn:
        all_files = [i for i in all_files if i.endswith(list_only_extn)]

    return all_files


def read_s3_object(s3_client, bucket_name, file_name):
    """
    Read an object without downloading it. (tested with JSON)

    :param s3_client: boto3 client pointer
    :type s3_client: <class botocore.client.S3>
    :param bucket_name: Name of bucket where the file is stored
    :type bucket_name: str
    :param file_name: name of the file to read. Can also contain the name of dir e.g. "dir/subdir/foo.json"
    :type file_name: str
    :return: pointer to read object
    """
    response = s3_client.get_object(Bucket=bucket_name, Key=file_name)
    content = response['Body'].read().decode('utf-8')
    return json.loads(content)
