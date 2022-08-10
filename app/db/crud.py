import typing

import sqlmodel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.engine.result import ScalarResult
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import abc


class DatabaseImpl(abc.Database):
    """Implementaion of a database connection for transacting and interacting with
    database tables —those that derive from SQLModel.
    """

    _engine: AsyncEngine

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

    @staticmethod
    async def update(
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

    async def create_table(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)

    async def add_row(self, table_model: sqlmodel.SQLModel) -> None:
        async with AsyncSession(self._engine) as session:
            session.add(table_model)
            await session.commit()

    async def remove_row(self, table_model: sqlmodel.SQLModel, attribute: str) -> None:
        model = type(table_model)

        async with AsyncSession(self._engine) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row: ScalarResult[typing.Any] = await session.exec(
                sqlmodel.select(model).where(  # type: ignore
                    getattr(model, attribute) == getattr(table_model, attribute)
                )  # type: ignore
            )
            await session.delete(row.one())
            await session.commit()

    async def get_row(
        self, table_model: sqlmodel.SQLModel, attribute: str, query: str
    ) -> ScalarResult[typing.Any]:
        row: ScalarResult[typing.Any]
        model = type(table_model)

        async with AsyncSession(self._engine) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row = await session.exec(
                sqlmodel.select(model).where(getattr(model, attribute) == query)  # type: ignore
            )

        return row

    async def get_all_row(
        self, table_model: sqlmodel.SQLModel
    ) -> ScalarResult[typing.Any]:
        model = type(table_model)

        async with AsyncSession(self._engine) as session:
            return await session.exec(sqlmodel.select(model))  # type: ignore

    async def update_row(self, table_model: sqlmodel.SQLModel, attribute: str) -> None:
        model = type(table_model)
        table = table_model.__dict__

        async with AsyncSession(self._engine) as session:
            row: ScalarResult[typing.Any] = await session.exec(
                sqlmodel.select(model).where(  # type: ignore
                    getattr(model, attribute) == getattr(table_model, attribute)
                )  # type: ignore
            )
            task = row.one()
            task = await self.update(task, table)

            session.add(task)
            await session.commit()
            await session.refresh(task)
