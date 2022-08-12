import uuid

import starlite
from starlette import datastructures

from app.services import imagekit


class TemplateService:
    CERTINIZE_BUCKET = "certinize-bucket"

    async def add_certificate_template(
        self,
        data: dict[str, datastructures.UploadFile],
        imagekit_client: imagekit.ImageKitClient,
    ):
        try:
            image_src = data["image"]
            return await imagekit_client.upload_file(
                image_src.file.read(),
                str(uuid.uuid1()),
                {"folder": self.CERTINIZE_BUCKET},
            )
        except KeyError as key_err:
            raise starlite.ValidationException(str(key_err)) from key_err
