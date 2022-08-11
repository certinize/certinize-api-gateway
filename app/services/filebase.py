"""
app.services.filebase
~~~~~~~~~~~~~~~~~~~~~

This module contains an async client that provides methods for interacting with
Filebase's S3-compatible API.
"""
from types_aiobotocore_s3 import client as s3client
from types_aiobotocore_s3 import type_defs


class Filebase:
    """Client implementation for Filebase's S3-compatible API."""

    @staticmethod
    async def create_bucket(
        client: s3client.S3Client, bucket: str
    ) -> type_defs.CreateBucketOutputTypeDef:
        """Create a new S3 bucket.

        Args:
            client (s3client.S3Client): A client representing S3.
            bucket (str): The name of the bucket to create.

        Returns:
            type_defs.CreateBucketOutputTypeDef: Create bucket output.
        """
        return await client.create_bucket(Bucket=bucket)

    @staticmethod
    async def put_object(
        client: s3client.S3Client, bucket: str, key: str, body: bytes
    ) -> type_defs.PutObjectOutputTypeDef:
        """Upload an object to an S3 bucket.

        Args:
            client (s3client.S3Client): A client representing S3.
            bucket (str): The bucket name of the bucket containing the object.
            key (str): Object key for which the PUT action was initiated.
            body (bytes): Object data.

        Returns:
            type_defs.PutObjectOutputTypeDef: Put object output.
        """
        return await client.put_object(Bucket=bucket, Key=key, Body=body)

    @staticmethod
    async def get_object(
        client: s3client.S3Client, bucket: str, key: str
    ) -> type_defs.GetObjectOutputTypeDef:
        """Delete an object from an S3 bucket.

        Args:
            client (s3client.S3Client): A client representing S3.
            bucket (str): Key of the object to get.
            key (str): Key name of the object to delete.

        Returns:
            type_defs.GetObjectOutputTypeDef: Get object output.
        """
        return await client.get_object(Bucket=bucket, Key=key)

    @staticmethod
    async def delete_object(
        client: s3client.S3Client, bucket: str, key: str
    ) -> type_defs.DeleteObjectOutputTypeDef:
        """Delete an object from an S3 bucket.

        Args:
            client (s3client.S3Client): A client representing S3.
            bucket (str): The bucket name of the bucket containing the object.
            key (str): Key name of the object to delete.

        Returns:
            type_defs.DeleteObjectOutputTypeDef: Delete object output.
        """
        return await client.delete_object(Bucket=bucket, Key=key)
