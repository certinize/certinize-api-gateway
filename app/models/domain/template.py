import base64
import binascii

import pydantic


class TemplateUpload(pydantic.BaseModel):
    image: list[str]

    @pydantic.validator("image")
    @classmethod
    def image_is_valid_base64(cls, value: list[str]):
        for index, image in enumerate(value):
            try:
                base64.b64decode(image)
            except binascii.Error as error:
                raise ValueError(
                    f"image at index {index} is not a valid base64 string"
                ) from error

        return value
