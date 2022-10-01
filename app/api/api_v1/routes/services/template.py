import asyncio
import typing
import uuid

import starlite

from app.db import crud
from app.models.domain import template
from app.models.schemas import templates
from app.services import object_processor

CERTINIZE_BUCKET = "certinize-bucket"
UPLOAD_OPTION = {"folder": CERTINIZE_BUCKET}

ImageKitStoreRes = dict[str, typing.Any] | dict[str, list[dict[str, typing.Any]]]


class TemplateService:
    async def _add_certificate_template(
        self, object_processor_: object_processor.ObjectProcessor, ecert: str
    ) -> dict[str, typing.Any]:
        try:
            return await object_processor_.upload_object(
                objectb=ecert,
                object_name=str(uuid.uuid1()),
                options=UPLOAD_OPTION,
            )
        except ConnectionError as err:
            raise starlite.HTTPException(status_code=502, detail=str(err))

    async def _create_template_schema(
        self,
        imagekit_response: dict[str, typing.Any],
        template_schema: type[templates.Templates],
    ) -> tuple[templates.Templates, dict[str, typing.Any]]:
        try:
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
        except KeyError as err:
            raise starlite.HTTPException(
                status_code=502,
                detail="invalid server response from object processor",
                extra=imagekit_response.get("detail") or imagekit_response,
            ) from err

        return (template_schema(**reusable_result), reusable_result)

    async def _store_imagekit_response(
        self,
        database: crud.DatabaseImpl,
        template_schema: type[templates.Templates],
        imagekit_response: dict[str, typing.Any] | list[dict[str, typing.Any]],
    ) -> ImageKitStoreRes:
        if isinstance(imagekit_response, dict):
            template_ = await self._create_template_schema(
                imagekit_response=imagekit_response, template_schema=template_schema
            )
            await database.add_row(template_[0])
            return template_[1]

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
        data: template.TemplateUpload,
        database: crud.DatabaseImpl,
        object_processor_: object_processor.ObjectProcessor,
        template_schema: type[templates.Templates],
    ) -> ImageKitStoreRes:
        image_src = data.image
        requests = [
            self._add_certificate_template(
                object_processor_=object_processor_, ecert=image
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
