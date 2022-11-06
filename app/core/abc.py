import abc
import typing

import sqlmodel
from sqlalchemy.engine import result as sqlalchemy_result
from sqlalchemy.ext import asyncio as sqlalchemy_asyncio
from sqlmodel.engine import result


class Database(abc.ABC):
    """Abstract base class of a database interface."""

    @abc.abstractmethod
    async def create_table(self, engine: sqlalchemy_asyncio.AsyncEngine) -> None:
        """Create physical tables for all the table models stored in
        `sqlmodel.SQLModel.metadata`.

        Args:
            engine (AsyncEngine): An asyncio proxy for `_engine.Engine`.
        """

    @abc.abstractmethod
    async def add(
        self, engine: sqlalchemy_asyncio.AsyncEngine, table_model: sqlmodel.SQLModel
    ) -> None:
        """Add a row to a database table.

        Args:
            engine (AsyncEngine): An asyncio proxy for `_engine.Engine`.
            table_model (sqlmodel.SQLModel): A subclass of sqlmodel.SQLModel.
        """

    @abc.abstractmethod
    async def delete(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        table_model: sqlmodel.SQLModel,
        attribute: str,
    ) -> None:
        """Remove a row from a database table.

        Args:
            engine (sqlalchemy_asyncio.AsyncEngine): An asyncio proxy for
                `_engine.Engine`.
            table_model (sqlmodel.SQLModel): A subclass of SQLModel
            attribute (str): A Table model attribute.
        """

    @abc.abstractmethod
    async def select(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        table_model: sqlmodel.SQLModel,
        attribute: str,
        query: str,
    ) -> result.ScalarResult[typing.Any]:
        """Select a row from a database table.

        Args:
            table_model (sqlmodel.SQLModel): A subclass of SQLModel.
            attribute (str): A Table model attribute.

        Returns:
            ScalarResult[Any]: A `ScalarResult` which contains a scalar value or
                sequence of scalar values.
        """

    @abc.abstractmethod
    async def select_all(
        self, engine: sqlalchemy_asyncio.AsyncEngine, table_model: sqlmodel.SQLModel
    ) -> result.ScalarResult[typing.Any]:
        """Fetch all records in a database table.

        Args:
            engine: (sqlalchemy_asyncio.AsyncEngine): An asyncio proxy for
                `_engine.Engine`.
            table_model (sqlmodel.SQLModel): Type of the class which corresponds to a
                database table.

        Returns:
            ScalarResult[typing.Any]: A `ScalarResult` which contains a scalar value or
                sequence of scalar values.
        """

    @abc.abstractmethod
    async def select_join(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        main_model: sqlmodel.SQLModel,
        *table_models: type[sqlmodel.SQLModel]
    ) -> result.ScalarResult[typing.Any] | None:
        """Select rows from multiple tables using a join.

        Args:
            engine: (sqlalchemy_asyncio.AsyncEngine): An asyncio proxy for
                `_engine.Engine`.
            main_model (sqlmodel.SQLModel): Type of the class which corresponds to a
                database table.
            table_models (type[sqlmodel.SQLModel]): Types of the classes which
                correspond to a database table.

        Returns:
            ScalarResult[typing.Any]: A `ScalarResult` which contains a scalar value or
                sequence of scalar values.
        """

    @abc.abstractmethod
    async def select_all_join(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        *table_models: type[sqlmodel.SQLModel] | sqlmodel.SQLModel,
    ) -> sqlalchemy_result.ChunkedIteratorResult | None:
        """Select all rows from multiple tables using a join.

        Args:
            engine: (sqlalchemy_asyncio.AsyncEngine): An asyncio proxy for
                `_engine.Engine`.
            table_models (type[sqlmodel.SQLModel]): Types of the classes which
                correspond to a database table.

        Returns:
            ChunkedIteratorResult: A `ChunkedIteratorResult` which contains a
                sequence of scalar values.
        """

    @abc.abstractmethod
    async def update(
        self,
        engine: sqlalchemy_asyncio.AsyncEngine,
        table_model: sqlmodel.SQLModel,
        attribute: str,
    ) -> None:
        """Update a database row.

        Args:
            table_model (sqlmodel.SQLModel): A subclass of SQLModel.
            attribute (str): A table model attribute.
        """
