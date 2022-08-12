import asyncio
import typing
import uuid

import starlite
from starlette import datastructures

from app.services import imagekit


class TemplateService:
    CERTINIZE_BUCKET = "certinize-bucket"

    async def _add_certificate_template(
        self, imagekit_client: imagekit.ImageKitClient, ecert: bytes
    ) -> dict[str, typing.Any]:
        file_name = str(uuid.uuid1())
        options = {"folder": self.CERTINIZE_BUCKET}

        return await imagekit_client.upload_file(
            file=ecert, file_name=file_name, options=options
        )

    async def add_certificate_template(
        self,
        data: dict[str, datastructures.UploadFile | list[datastructures.UploadFile]],
        imagekit_client: imagekit.ImageKitClient,
    ):
        try:
            image_src = data["image"]

            if isinstance(image_src, datastructures.UploadFile):
                await self._add_certificate_template(
                    imagekit_client=imagekit_client, ecert=image_src.file.read()
                )

            if isinstance(image_src, list):
                requests = [
                    self._add_certificate_template(
                        imagekit_client=imagekit_client,
                        ecert=image.file.read(),
                    )
                    for image in image_src
                ]
                await asyncio.gather(*requests)
        except KeyError as key_err:
            raise starlite.ValidationException(
                "key missing from request body: image"
            ) from key_err
