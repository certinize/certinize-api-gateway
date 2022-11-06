import typing

import starlite
from sqlalchemy.ext.asyncio import engine

from app.api.api_v1.dependencies import associated_services
from app.api.api_v1.dependencies import database as database_deps
from app.api.api_v1.routes.services import template as template_svcs
from app.core import abc
from app.models.domain import template
from app.services import object_processor


class TemplateController(starlite.Controller):
    path = "/templates"

    dependencies: dict[str, "starlite.Provide"] | None = {
        "database": starlite.Provide(database_deps.get_templates_repository),
        "db_engine": starlite.Provide(database_deps.get_db_engine),
        "object_processor_": starlite.Provide(
            associated_services.get_object_processor_client
        ),
        "template_service": starlite.Provide(template_svcs.TemplateService),
    }

    @starlite.post()
    async def add_certificate_template(  # pylint: disable=R0913
        self,
        data: template.TemplateUpload,
        database: abc.Database,
        db_engine: engine.AsyncEngine,
        object_processor_: object_processor.ObjectProcessor,
        template_service: template_svcs.TemplateService,
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> template_svcs.ImageKitStoreRes:
        return await template_service.add_certificate_template(
            data,
            database,
            db_engine,
            object_processor_,
            token,
        )

    @starlite.get()
    async def list_certificate_templates(
        self,
        database: abc.Database,
        db_engine: engine.AsyncEngine,
        template_service: template_svcs.TemplateService,
        token: str = starlite.Parameter(header="X-API-KEY", min_length=36),
    ) -> dict[str, list[typing.Any]]:
        result = await template_service.list_certificate_templates(
            database,
            db_engine,
            token,
        )

        return {"templates": result.all()}
