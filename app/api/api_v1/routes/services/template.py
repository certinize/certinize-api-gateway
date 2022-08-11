import starlite
from starlette import datastructures


class TemplateService:
    async def add_certificate_template(
        self, data: dict[str, datastructures.UploadFile]
    ):
        image_src: datastructures.UploadFile

        try:
            image_src = data["image"]
        except KeyError as err:
            raise starlite.ValidationException(str(err)) from err

        return
