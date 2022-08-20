import asyncio
import json
import typing
import uuid

import starlite
from starlette import datastructures

from app.db import crud
from app.models.schemas import templates
from app.services import image_processor

CERTINIZE_BUCKET = "certinize-bucket"


class TemplateService:
    async def _add_certificate_template(
        self, image_processor_: image_processor.ImageProcessor, ecert: bytes
    ) -> dict[str, typing.Any]:
        options = {"folder": CERTINIZE_BUCKET}

        try:
            return await image_processor_.upload_file(
                imageb=ecert,
                image_name=str(uuid.uuid1()),
                options=json.dumps(options),
            )
        except ConnectionError as err:
            raise starlite.HTTPException(status_code=502, detail=str(err))

    async def _create_template_schema(
        self,
        imagekit_response: dict[str, typing.Any],
        template_schema: type[templates.Templates],
    ) -> tuple[templates.Templates, dict[str, typing.Any]]:
        reusable_result = dict(
            template_height=imagekit_response["height"],
            template_id=uuid.uuid1(),
            template_name=imagekit_response["name"],
            template_path=imagekit_response["filePath"],
            template_size=imagekit_response["size"],
            template_thumbnail_url=imagekit_response["thumbnailUrl"],
            template_url=imagekit_response["url"],
            template_width=imagekit_response["width"],
        )

        return (template_schema(**reusable_result), reusable_result)

    async def _store_imagekit_response(
        self,
        database: crud.DatabaseImpl,
        template_schema: type[templates.Templates],
        imagekit_response: dict[str, typing.Any] | list[dict[str, typing.Any]],
    ):
        if isinstance(imagekit_response, dict):
            template = await self._create_template_schema(
                imagekit_response=imagekit_response, template_schema=template_schema
            )
            await database.add_row(template[0])
            return template[1]

        templates_ = [
            await self._create_template_schema(
                imagekit_response=image, template_schema=template_schema
            )
            for image in imagekit_response
        ]
        insert_templates_op = [database.add_row(template[0]) for template in templates_]

        await asyncio.gather(*insert_templates_op)
        return {"templates": [template[1] for template in templates_]}

    async def add_certificate_template(
        self,
        data: dict[str, datastructures.UploadFile | list[datastructures.UploadFile]],
        database: crud.DatabaseImpl,
        image_processor_: image_processor.ImageProcessor,
        template_schema: type[templates.Templates],
    ):
        image_src: datastructures.UploadFile | list[datastructures.UploadFile]

        try:
            image_src = data["image"]
        except KeyError as key_err:
            raise starlite.ValidationException(
                "key missing from request body: image"
            ) from key_err

        if isinstance(image_src, datastructures.UploadFile):
            imagekit_resp = await self._add_certificate_template(
                image_processor_=image_processor_, ecert=image_src.file.read()
            )
        else:
            requests = [
                self._add_certificate_template(
                    image_processor_=image_processor_, ecert=image.file.read()
                )
                for image in image_src
            ]
            imagekit_resp = await asyncio.gather(*requests)

        return await self._store_imagekit_response(
            database=database,
            template_schema=template_schema,
            imagekit_response=imagekit_resp,
        )

    async def list_certificate_templates(
        self, database: crud.DatabaseImpl, templates_schema: type[templates.Templates]
    ):
        return await database.select_all_row(templates_schema)
