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
from app.models.schemas import configurations, templates


class ConfigurationService:
    async def create_template_config(
        self,
        data: configuration.TemplateConfiguration,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        token: str,
        /,
    ) -> dict[str, typing.Any]:
        template_id = data.template_id
        config_meta = data.dict()
        template_config_id = uuid.uuid1()

        # Reusing a variable seems more efficient and correct than extracting the value
        # from the dict everytime we need it.
        template_config_name = config_meta["template_config_name"]

        # SQLAlchemy rejects objects, so convert them to their string reprs.
        config_meta["template_id"] = str(config_meta["template_id"])

        # Delete unsued fields
        del config_meta["template_config_name"]
        del config_meta["template_id"]

        try:
            await database.add(
                engine,
                configurations.Configurations(
                    template_config_id=template_config_id,
                    api_key=uuid.UUID(token),
                    config_meta=config_meta,
                    template_config_name=template_config_name,
                    template_id=template_id,
                ),
            )
        except exc.IntegrityError as integrity_err:
            raise starlite.HTTPException(
                status_code=400,
                detail=f"Template does not exist: {template_id=}",
            ) from integrity_err

        return {
            "template_config_id": template_config_id,
            "template_config_name": template_config_name,
            "config_meta": {
                "recipient_name_meta": config_meta["recipient_name_meta"],
            },
            "template_id": template_id,
        }

    async def get_template_config(  # pylint: disable=R0913
        self,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        template_config_id: pydantic.UUID1,
        token: str,
        /,
    ) -> dict[str, typing.Any]:

        try:
            results = await database.select_join(
                engine,
                configurations.Configurations(
                    template_config_id=template_config_id,
                    api_key=uuid.UUID(token),
                    template_config_name="",
                ),
                configurations.Configurations,
                templates.Templates,
            )
            assert results is not None
            results_ = results.one()

            return {
                "template_config": results_["Configurations"].dict(),
                "template": results_["Templates"].dict(),
            }
        except exc.NoResultFound as err:
            raise starlite.NotFoundException(str(err)) from err

    async def list_template_config(  # pylint: disable=R0913
        self,
        database: abc.Database,
        engine: sqlalchemy_asyncio.AsyncEngine,
        token: str,
        /,
    ) -> dict[str, list[dict[str, dict[str, typing.Any]]]]:
        results = await database.select_all_join(
            engine,
            configurations.Configurations(
                template_config_id=uuid.uuid1(),
                api_key=uuid.UUID(token),
                template_config_name="",
            ),
            templates.Templates,
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
                    "template": results["Templates"].dict(),
                    "template_config": template_config,
                }
            )

        return {"configurations": serialized_results}
