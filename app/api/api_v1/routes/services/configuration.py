import typing
import uuid

import pydantic
import starlite
from sqlalchemy import exc

from app.db import crud
from app.models.domain import configuration
from app.models.schemas import configurations


class ConfigurationService:
    async def create_template_config(
        self,
        data: configuration.TemplateConfiguration,
        certificate_config_schema: type[configurations.TemplateConfigurations],
        database: crud.DatabaseImpl,
    ) -> dict[str, uuid.UUID | typing.Any]:
        config_meta = data.__dict__
        template_config_id = uuid.uuid1()

        # Reusing a variable seems more efficient and correct than extracting the value
        # from the dict everytime we need it.
        template_config_name = config_meta["template_config_name"]
        del config_meta["template_config_name"]

        # SQLAlchemy rejects objects, so convert them to their string reprs.
        config_meta["template_id"] = str(config_meta["template_id"])
        config_meta["font_id"] = str(config_meta["font_id"])

        try:
            certificate_config = await database.get_row(
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
                    "font_id": config_meta["font_id"],
                },
            }

    async def get_template_config(
        self,
        template_config_id: pydantic.UUID1,
        certificate_config_schema: type[configurations.TemplateConfigurations],
        database: crud.DatabaseImpl,
    ):
        try:
            certificate_config = await database.get_row(
                certificate_config_schema(template_config_name=""),
                "template_config_id",
                str(template_config_id),
            )
            return certificate_config.one()
        except exc.NoResultFound as err:
            raise starlite.NotFoundException(str(err)) from err

    async def list_template_config(
        self,
        certificate_config_schema: type[configurations.TemplateConfigurations],
        database: crud.DatabaseImpl,
    ):
        result = await database.get_all_row(
            certificate_config_schema(template_config_name="")
        )

        return {"configurations": result.all()}
