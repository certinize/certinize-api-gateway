import asyncio
import typing
import uuid

import pydantic
import starlite
from sqlalchemy.ext.asyncio import engine

from app import utils
from app.core import abc
from app.models.domain import template
from app.models.schemas import templates
from app.services import object_processor

CERTINIZE_BUCKET = "certinize-bucket"
UPLOAD_OPTION = {"folder": CERTINIZE_BUCKET}

ImageKitStoreRes: typing.TypeAlias = (
    dict[str, typing.Any] | dict[str, list[dict[str, typing.Any]]]
)


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
        self, imagekit_response: dict[str, typing.Any], token: str, /
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
                api_key=token,
            )
        except KeyError as err:
            raise starlite.HTTPException(
                status_code=502,
                detail="invalid server response from object processor",
                extra=imagekit_response.get("detail") or imagekit_response,
            ) from err

        return (templates.Templates(**reusable_result), reusable_result)

    async def _store_imagekit_response(
        self,
        database: abc.Database,
        db_engine: engine.AsyncEngine,
        imagekit_response: dict[str, typing.Any] | list[dict[str, typing.Any]],
        token: str,
        /,
    ) -> ImageKitStoreRes:
        if isinstance(imagekit_response, dict):
            template_ = await self._create_template_schema(imagekit_response, token)
            await database.add(db_engine, template_[0])
            return template_[1]

        templates_ = [
            await self._create_template_schema(image, token)
            for image in imagekit_response
        ]
        insert_templates_op = [
            database.add(db_engine, template[0]) for template in templates_
        ]

        await asyncio.gather(*insert_templates_op)
        return {"templates": [template[1] for template in templates_]}

    async def add_certificate_template(
        self,
        data: template.TemplateUpload,
        database: abc.Database,
        db_engine: engine.AsyncEngine,
        object_processor_: object_processor.ObjectProcessor,
        token: str,
        /,
    ) -> ImageKitStoreRes:
        image_src = data.templates
        requests = [
            self._add_certificate_template(
                object_processor_=object_processor_, ecert=image
            )
            for image in image_src
        ]
        imagekit_resp = await asyncio.gather(*requests)

        return await self._store_imagekit_response(
            database, db_engine, imagekit_resp, token
        )

    async def list_certificate_templates(
        self,
        database: abc.Database,
        db_engine: engine.AsyncEngine,
        token: str,
        /,
    ):
        template_ = templates.Templates(
            api_key=pydantic.UUID5(token),
            template_url=pydantic.HttpUrl("", scheme="https"),
            template_thumbnail_url=pydantic.HttpUrl("", scheme="https"),
            template_name="",
            template_path="",
            template_id=uuid.uuid1(),
            template_size=pydantic.ByteSize(0),
            template_width=0,
            template_height=0,
        )

        await utils.check_api_key_exists(database, db_engine, token)

        return await database.select_all(db_engine, template_)
