# pylint: disable=R0801
import dataclasses
import typing

import sqlmodel
from sqlalchemy.engine import result as sqlalchemy_result
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio
from sqlmodel.engine import result
from sqlmodel.ext.asyncio import session
from sqlmodel.sql import expression

from app.core import abc
from app.models.schemas import configurations, templates


@dataclasses.dataclass
class ConfigRepoAttribs:
    template_config_id: dict[str, str]
    api_key: dict[str, str]


class ConfigurationsRepository(abc.Database):
    """Database implementation for the configurations table."""

    def __init__(self) -> None:
        # Avoid an SAWarning. See: https://github.com/tiangolo/sqlmodel/issues/189
        expression.SelectOfScalar.inherit_cache = True  # type: ignore
        expression.Select.inherit_cache = True  # type: ignore

    @staticmethod
    def update_attrib(
        instance: typing.Any, update: dict[typing.Any, typing.Any]
    ) -> typing.Any:
        """Overwrite value of class attribute.

        Args:
            instance (typing.Any): A class instance.
            update (dict[typing.Any, typing.Any]): A dictionary containing the
                attributes to be overwritten.

        Returns:
            typing.Any: A class instance with updated attribute values.
        """
        for key, value in update.items():
            setattr(instance, key, value)
        return instance

    async def create_table(self, engine: sqlalchemy_asyncio.AsyncEngine) -> None:
        async with engine.begin() as conn:
            await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)

    async def add(
        self, engine: sqlalchemy_asyncio.AsyncEngine, table_model: sqlmodel.SQLModel
    ) -> None:
        async with session.AsyncSession(engine) as async_session:
            async_session.add(table_model)
            await async_session.commit()

    async def delete(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        table_model: sqlmodel.SQLModel,
        attribute: str,
    ) -> None:
        model = type(table_model)

        async with session.AsyncSession(engine) as async_session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: result.ScalarResult[typing.Any] = await async_session.exec(
                sqlmodel.select(model).where(  # type: ignore
                    getattr(model, attribute) == getattr(table_model, attribute)
                )
            )
            await async_session.delete(row.one())
            await async_session.commit()

    async def select(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        table_model: sqlmodel.SQLModel,
        attribute: str,
        query: str,
    ) -> result.ScalarResult[typing.Any]:
        model = type(table_model)

        async with session.AsyncSession(engine) as async_session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: result.ScalarResult[typing.Any] = await async_session.exec(
                sqlmodel.select(model).where(  # type: ignore
                    getattr(model, attribute) == query
                )
            )

        return row

    async def select_all(
        self, engine: sqlalchemy_asyncio.AsyncEngine, table_model: sqlmodel.SQLModel
    ) -> result.ScalarResult[typing.Any]:
        model = type(table_model)

        async with session.AsyncSession(engine) as async_session:
            return await async_session.exec(sqlmodel.select(model))  # type: ignore

    async def select_join(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        main_model: sqlmodel.SQLModel,
        *table_models: type[sqlmodel.SQLModel],
    ) -> result.ScalarResult[typing.Any]:
        templts = table_models[1]

        assert isinstance(main_model, configurations.Configurations)

        # We only need three table models for the join: the configurations schema and
        # the templates schema. We don't have to check for the configurations schema as
        # the assertions for the templates schema should do that.
        assert isinstance(templts, type(templates.Templates))

        queries = ConfigRepoAttribs(template_config_id={}, api_key={})

        # Dynamically get the str repr of the attribs (attributes) and their values
        # (queries), so that we don't have to ask the user for them.
        for var in vars(main_model):
            if "template_config_id" in var:
                queries.template_config_id["attrib"] = var
                queries.template_config_id["value"] = getattr(main_model, var)

            if "api_key" in var:
                queries.api_key["attrib"] = var
                queries.api_key["value"] = getattr(main_model, var)

        async with session.AsyncSession(engine) as async_session:
            return await async_session.exec(
                sqlmodel.select(*table_models)  # type: ignore
                .where(
                    getattr(type(main_model), queries.api_key["attrib"])
                    == main_model.api_key
                )
                .where(
                    getattr(type(main_model), queries.template_config_id["attrib"])
                    == main_model.template_config_id
                )
                .join(templts)
            )

    async def select_all_join(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        *table_models: type[sqlmodel.SQLModel] | sqlmodel.SQLModel,
    ) -> sqlalchemy_result.ChunkedIteratorResult:
        configs = table_models[0]
        templts = table_models[1]
        queries = ConfigRepoAttribs(template_config_id={}, api_key={})

        # Ensure we pass a column expression or FROM clause to select().
        from_clause = (type(configs), templts)

        assert isinstance(configs, configurations.Configurations)
        assert isinstance(templts, type(templates.Templates))

        for var in vars(configs):
            if "api_key" in var:
                queries.api_key["attrib"] = var
                queries.api_key["value"] = getattr(configs, var)

        async with session.AsyncSession(engine) as async_session:
            return await async_session.exec(
                sqlmodel.select(*from_clause)  # type: ignore
                .where(
                    getattr(type(configs), queries.api_key["attrib"]) == configs.api_key
                )
                .join(templts)
            )

    async def update(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        table_model: sqlmodel.SQLModel,
        attribute: str,
    ) -> None:
        model = type(table_model)
        table = table_model.__dict__

        async with session.AsyncSession(engine) as async_session:
            row: result.ScalarResult[typing.Any] = await async_session.exec(
                sqlmodel.select(model).where(  # type: ignore
                    getattr(model, attribute) == getattr(table_model, attribute)
                )
            )
            task = row.one()
            task = self.update_attrib(task, table)

            async_session.add(task)
            await async_session.commit()
            await async_session.refresh(task)
