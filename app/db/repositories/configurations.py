import typing

import sqlmodel
from sqlalchemy.engine import result as sqlalchemy_result
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio
from sqlmodel.engine import result
from sqlmodel.ext.asyncio import session

from app.core import abc
from app.models.schemas import configurations, fonts, templates


class ConfigurationsRepository(abc.Database):
    """Database implementation for the configurations table."""

    @staticmethod
    def update(
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

    async def add_row(
        self, engine: sqlalchemy_asyncio.AsyncEngine, table_model: sqlmodel.SQLModel
    ) -> None:
        async with session.AsyncSession(engine) as async_session:
            async_session.add(table_model)
            await async_session.commit()

    async def delete_row(
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

    async def select_row(
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

    async def select_all_row(
        self, engine: sqlalchemy_asyncio.AsyncEngine, table_model: sqlmodel.SQLModel
    ) -> result.ScalarResult[typing.Any]:
        model = type(table_model)

        async with session.AsyncSession(engine) as async_session:
            return await async_session.exec(sqlmodel.select(model))  # type: ignore

    async def select_join(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        main_model: sqlmodel.SQLModel,
        *table_models: type[sqlmodel.SQLModel]
    ) -> result.ScalarResult[typing.Any]:
        attribute = ""
        query = ""

        # We only need three table models for the join: the configurations schema, the
        # fonts schema, and the templates schema. We don't have to check for the
        # configurations schema as the assertions for the other two tables should do
        # that.
        assert isinstance(table_models[1], type(fonts.Fonts))
        assert isinstance(table_models[2], type(templates.Templates))

        # Dynamically get the str repr of the first "id" attrib (attribute) and its
        # value (query), so that we don't have to ask the user for them.
        for var in vars(main_model):
            if "_id" in var:
                attribute = var
                query = getattr(main_model, attribute)
                break

        async with session.AsyncSession(engine) as async_session:
            return await async_session.exec(
                sqlmodel.select(*table_models)  # type: ignore
                .join(table_models[1])
                .join(table_models[2])
                .where(getattr(type(main_model), attribute) == query)
            )

    async def select_all_join(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        *table_models: type[sqlmodel.SQLModel]
    ) -> sqlalchemy_result.ChunkedIteratorResult:
        assert isinstance(table_models[0], type(configurations.Configurations))
        assert isinstance(table_models[1], type(fonts.Fonts))
        assert isinstance(table_models[2], type(templates.Templates))

        async with session.AsyncSession(engine) as async_session:
            return await async_session.exec(
                sqlmodel.select(*table_models)  # type: ignore
                .join(table_models[1])
                .join(table_models[2])
            )

    async def update_row(
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
            task = self.update(task, table)

            async_session.add(task)
            await async_session.commit()
            await async_session.refresh(task)
