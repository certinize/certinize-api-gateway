import uuid

import starlite
from starlette import datastructures
from types_aiobotocore_s3 import client

from app.services import filebase


class IssuanceService:
    @staticmethod
    async def transfer_certificate(
        data: dict[str, datastructures.UploadFile],
        filebase_client: filebase.FilebaseClient,
        s3_client: client.S3Client,
    ):
        # TODO: Upload certificate to IPFS, then transfer token
        try:
            image_src = data["image"]
            key = str(uuid.uuid1())
            output = await filebase_client.put_object(
                s3_client,
                bucket="certinize-bucket",
                key=key,
                body=image_src.file.read(),
            )
            return output["ETag"]
        except KeyError as key_err:
            raise starlite.ValidationException(str(key_err)) from key_err
