"""
Multi-threading
==================
Module for multi-threading upload and download operations (IO bound tasks) for AWS S3 bucket.
"""

import logging
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from glob import glob

from rich.traceback import install
from utils.s3 import list_s3_files, download_object, upload_objects

# Instantiating logger
LOGGER = logging.getLogger(__name__)

# instantiating rich traceback
install(show_locals=True)


class bulkUpload:
    def __init__(self, s3_client, upload_bucket, local_data_dir, s3_dir_path, file_type=".csv"):
        """
        Init method

        :param s3_client: boto3 pointer
        :param upload_bucket: name of target s3 bucket where export will be made
        :param local_data_dir: path where all files are stored (to be uploaded)
        :param s3_dir_path: name of directory in s3 where the data will be exported (can be empty string)
        :param file_type: type of files to be uploaded to s3. Default is `.csv`
        """
        self.s3_client = s3_client
        self.upload_bucket = upload_bucket
        self.local_data_dir = local_data_dir
        self.s3_dir_path = s3_dir_path
        self.file_type = file_type

        # contains path with file name
        self.files_to_upld = [g for g in glob(f'{self.local_data_dir}/*{self.file_type}')]
        LOGGER.debug(f"Total {len(self.files_to_upld)} queued for upload.")

        # Input to class
        self.__repr__()

    def serial_upload(self):
        LOGGER.info(f"Serialized mode for upload chosen. Files will be uploaded one by one.")
        for _file in self.files_to_upld:
            upload_objects(_file, self.s3_client, self.upload_bucket, self.s3_dir_path)

        LOGGER.info(f"All {len(self.files_to_upld)} files uploaded from {self.local_data_dir}")

    def multi_threaded_upld(self):
        LOGGER.info(f"Multi-threaded mode for file upload chosen. Getting threads ready!.")
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            list(executor.map(partial(upload_objects,
                                      s3_client=self.s3_client, export_bucket=self.upload_bucket,
                                      upload_dir_name=self.s3_dir_path), self.files_to_upld))

            LOGGER.info(f"All {len(self.files_to_upld)} files uploaded from {self.local_data_dir}")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.s3_client}, {self.upload_bucket}, {self.local_data_dir}, " \
               f"{self.s3_dir_path}, {self.file_type})"


class bulkDownload:
    def __init__(self, s3_client, download_bucket, bucket_dir, save_path):
        """
        Init method

        :param s3_client: boto3 pointer
        :param download_bucket: name of bucket from where the data will be downloaded
        :param bucket_dir: name of dir where data is present in bucket. If data is present in root, use empty str ("")
        or None as arguments; this downloads entire bucket.
        :param save_path: local path where the data files will be downloaded
        """

        self.s3_client = s3_client
        self.download_bucket = download_bucket
        self.bucket_dir = bucket_dir
        self.save_path = save_path

        self.files_to_dwld = list_s3_files(self.s3_client, self.download_bucket, self.bucket_dir)
        LOGGER.debug(f"Total {len(self.files_to_dwld)} files queued for download.")

        # Input to class
        self.__repr__()

    def serial_download(self):
        LOGGER.info(f"Serialized mode for download chosen. Files will be downloaded one by one.")
        for _file in self.files_to_dwld:
            download_object(_file, self.s3_client, self.download_bucket, self.save_path)

        LOGGER.info(f"All {len(self.files_to_dwld)} files downloaded to {self.save_path}")
        return self.files_to_dwld

    def multi_threaded_dwld(self):
        LOGGER.info(f"Multi-threaded mode for file download chosen. Getting threads ready.")
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            list(executor.map(partial(download_object, s3_client=self.s3_client, s3_bucket=self.download_bucket,
                                      download_dir=self.save_path), self.files_to_dwld))

        LOGGER.info(f"All {len(self.files_to_dwld)} files downloaded to {self.save_path}")
        return self.files_to_dwld

    def __repr__(self):
        return f"{self.__class__.__name__}({self.s3_client}, {self.download_bucket}, {self.bucket_dir}, " \
               f"{self.save_path})"
