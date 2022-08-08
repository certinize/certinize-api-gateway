import typing
import uuid

import starlite
from sqlalchemy import exc

from app.db import crud
from app.models.domain import template
from app.models.schemas import templates


class ConfigurationService:
    async def create_template_config(
        self,
        data: template.TemplateConfigSave,
        certificate_config_schema: type[templates.TemplateConfiguration],
        database: crud.DatabaseImpl,
    ) -> dict[str, uuid.UUID | typing.Any]:
        config_meta = data.__dict__
        template_config_id = uuid.uuid1()
        template_config_name = config_meta["template_config_name"]
        del config_meta["template_config_name"]

        try:
            certificate_config = await database.select_row(
                certificate_config_schema(template_config_name=""),
                "template_config_name",
                template_config_name,
            )
            return certificate_config.one()
        except exc.NoResultFound:
            await database.add_row(
                certificate_config_schema(
                    template_config_id=template_config_id,
                    config_meta=config_meta,
                    template_config_name=template_config_name,
                )
            )
            return {
                "template_config_id": template_config_id,
                "template_config_name": template_config_name,
                "config_meta": {
                    "recipient_name": config_meta["recipient_name"],
                    "issuance_date": config_meta["issuance_date"],
                    "template_id": config_meta["template_id"],
                },
            }

    async def get_template_config(
        self,
        template_config_id: str,
        certificate_config_schema: type[templates.TemplateConfiguration],
        database: crud.DatabaseImpl,
    ):
        try:
            certificate_config = await database.select_row(
                certificate_config_schema(template_config_name=""),
                "template_config_id",
                template_config_id,
            )
            return certificate_config.one()
        except exc.NoResultFound as err:
            raise starlite.NotFoundException(err) from err
