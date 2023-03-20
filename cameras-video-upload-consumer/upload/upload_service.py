import boto3
import logging
import os
import pathlib

from boto3.exceptions import S3UploadFailedError
from upload.abstract_upload_service import AbstractUploadService


class AWSUploadService(AbstractUploadService):
    """Service to upload files to AWS S3"""

    def __init__(self, bucket: str = None):
        self._bucket_name = bucket or os.getenv('AWS_BUCKET_FOR_VIDEO')

        self._s3 = boto3.resource('s3')
        self.bucket = self._s3.Bucket(self._bucket_name)

    def upload(self, filepath):
        try:
            object_name = os.path.basename(filepath)
            response = self.bucket.upload_file(filepath, object_name)
            logging.info(os.getenv(response))
            logging.info(f"File {filepath} uploaded as {object_name} "
                         f"to {self._bucket_name}!")
        except S3UploadFailedError:
            # todo add behaviour to handle S3 issues during an uploading process
            """
                if something goes wrong, we can resend the message to the queue 
                and try to send the file again. We can also add an additional 
                key to the JSON message with a number indicating the number 
                of attempts to send the file to S3. We can also set up 
                a handler for sending a single file with a limit on the number 
                of attempts.
            """
            logging.info(f"S3 issue")
        except Exception as e:
            logging.error(f"Error while uploading {filepath} to S3: {e}")
