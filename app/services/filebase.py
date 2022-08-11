"""
app.services.filebase
~~~~~~~~~~~~~~~~~~~~~

This module contains an async client that provides methods for interacting with 
Filebase's S3-compatible API.
"""
from types_aiobotocore_s3 import client as s3client
from types_aiobotocore_s3 import type_defs


class Filebase:
    async def create_bucket(
        self, client: s3client.S3Client, bucket: str
    ) -> type_defs.CreateBucketOutputTypeDef:
        """Create a new S3 bucket.

        Args:
            client (s3client.S3Client): A client representing S3.
            bucket (str): The name of the bucket to create.

        Returns:
            type_defs.CreateBucketOutputTypeDef: A dictionary containing the location
                of the bucket and response metadata.
        """

        return await client.create_bucket(Bucket=bucket)
