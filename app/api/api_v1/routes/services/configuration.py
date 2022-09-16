# orjson raises E0611 and E1101
# pylint: disable=E1101

import typing
import uuid

import pydantic
import starlite
from sqlalchemy import exc
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio

from app.core import abc
from app.models.domain import configuration
from app.models.schemas import configurations, fonts, templates


class ConfigurationService:
    async def create_template_config(
        self,
        configs_schema: type[configurations.Configurations],
        data: configuration.TemplateConfiguration,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
    ) -> dict[str, typing.Any]:
        font_id = data.font_id
        template_id = data.template_id
        config_meta = data.dict()
        template_config_id = uuid.uuid1()

        # Reusing a variable seems more efficient and correct than extracting the value
        # from the dict everytime we need it.
        template_config_name = config_meta["template_config_name"]

        # SQLAlchemy rejects objects, so convert them to their string reprs.
        config_meta["template_id"] = str(config_meta["template_id"])
        config_meta["font_id"] = str(config_meta["font_id"])

        # Delete unsued fields
        del config_meta["font_id"]
        del config_meta["template_config_name"]
        del config_meta["template_id"]

        try:
            certificate_config = await database.select_row(
                engine,
                configs_schema(template_config_name=""),
                "template_config_name",
                template_config_name,
            )

            return certificate_config.one().dict()
        except exc.NoResultFound:
            await database.add_row(
                engine,
                configs_schema(
                    template_config_id=template_config_id,
                    config_meta=config_meta,
                    template_config_name=template_config_name,
                    font_id=font_id,
                    template_id=template_id,
                ),
            )

            return {
                "template_config_id": template_config_id,
                "template_config_name": template_config_name,
                "config_meta": {
                    "recipient_name_meta": config_meta["recipient_name_meta"],
                    "issuance_date_meta": config_meta["issuance_date_meta"],
                },
                "template_id": font_id,
                "font_id": template_id,
            }

    async def get_template_config(  # pylint: disable=R0913
        self,
        configs_schema: type[configurations.Configurations],
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        fonts_schema: type[fonts.Fonts],
        template_config_id: pydantic.UUID1,
        templates_schema: type[templates.Templates],
    ) -> dict[str, typing.Any]:
        try:
            results = await database.select_join(
                engine,
                configs_schema(
                    template_config_id=template_config_id, template_config_name=""
                ),
                configs_schema,
                fonts_schema,
                templates_schema,
            )
            assert results is not None
            results_ = results.one()

            return {
                "template_config": results_["Configurations"].dict(),
                "template": results_["Templates"].dict(),
                "font": results_["Fonts"].dict(),
            }
        except exc.NoResultFound as err:
            raise starlite.NotFoundException(str(err)) from err

    async def list_template_config(  # pylint: disable=R0913
        self,
        configs_schema: type[configurations.Configurations],
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        fonts_schema: type[fonts.Fonts],
        templates_schema: type[templates.Templates],
    ) -> dict[str, list[dict[str, dict[str, typing.Any]]]]:
        results = await database.select_all_join(
            engine, configs_schema, templates_schema, fonts_schema
        )
        serialized_results: list[dict[str, dict[str, typing.Any]]] = []

        assert results is not None

        for results in results.all():
            # In case this becomes confusing, here's what happens here:
            # 1. Convert the Row to its JSON representation.
            # 2. Deserialize the JSON repr using orjson.loads().
            # 3. Use SortedDict to sort the contents of the dict.
            # 4. Convert the SortedDict object to dict using dict().
            # 5. Assign the result to a parent dict key.
            # 6. Append the parent dict to serialized_results.

            template_config = results["Configurations"].dict()
            template_config_id = template_config["template_config_id"]
            template_config_name = template_config["template_config_name"]

            del template_config["template_config_id"]
            del template_config["template_config_name"]

            serialized_results.append(
                {
                    "template_config_id": template_config_id,
                    "template_config_name": template_config_name,
                    "font": results["Fonts"].dict(),
                    "template": results["Templates"].dict(),
                    "template_config": template_config,
                }
            )

        return {"configurations": serialized_results}
