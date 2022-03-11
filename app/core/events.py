from typing import Any, Callable, Coroutine

from starlite import State

from app.db.events import create_db_engine, dispose_db_engine, create_db_tables


def get_start_app_handler(
    state: State,
) -> Callable[..., Coroutine[Any, Any, None]]:
    async def start_app() -> None:
        await create_db_engine(state)
        await create_db_tables(state)

    return start_app


def get_stop_app_handler(state: State) -> Callable:  # type: ignore
    async def stop_app() -> None:
        await dispose_db_engine(state)

    return stop_app
