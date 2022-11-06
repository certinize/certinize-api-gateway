import typing

import sqlmodel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.engine.result import ScalarResult
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql import expression


class DatabaseImpl:
    """Implementaion of a database connection for transacting and interacting with
    database tables —those that derive from SQLModel.
    """

    _engine: AsyncEngine

    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine

        # Avoid an SAWarning. See: https://github.com/tiangolo/sqlmodel/issues/189
        expression.SelectOfScalar.inherit_cache = True  # type: ignore
        expression.Select.inherit_cache = True  # type: ignore

    async def create_table(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)

    async def add(self, table_model: sqlmodel.SQLModel) -> None:
        async with AsyncSession(self._engine) as session:
            session.add(table_model)
            await session.commit()

    async def delete(self, table_model: sqlmodel.SQLModel, attribute: str) -> None:
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

    async def select(
        self, table_model: sqlmodel.SQLModel, attribute: str, query: str
    ) -> ScalarResult[typing.Any]:
        row: ScalarResult[typing.Any]
        model = type(table_model)

        async with AsyncSession(self._engine) as session:
            # Temp ignore incompatible type passed to `exec()`. See:
            # https://github.com/tiangolo/sqlmodel/issues/54
            # https://github.com/tiangolo/sqlmodel/pull/58
            row = await session.exec(
                sqlmodel.select(model).where(  # type: ignore
                    getattr(model, attribute) == query
                )
            )

        return row

    async def select_all(
        self, table_model: sqlmodel.SQLModel | type[sqlmodel.SQLModel]
    ) -> ScalarResult[typing.Any]:
        if isinstance(table_model, sqlmodel.SQLModel):
            model = type(table_model)
        else:
            model = table_model

        async with AsyncSession(self._engine) as session:
            return await session.exec(sqlmodel.select(model))  # type: ignore

    async def update(
        self, table_model: sqlmodel.SQLModel, attribute: str, primary_key: str | int
    ) -> None:
        model = type(table_model)
        table = table_model.dict()

        async with AsyncSession(self._engine) as session:
            await session.exec(
                sqlmodel.update(model)
                .where(getattr(model, attribute) == primary_key)
                .values(table)  # type: ignore
            )
            await session.commit()
