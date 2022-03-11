from starlite import State

from app.db.events import create_db_engine, dispose_db_engine


def get_start_app_handler():
    async def start_app(state: State) -> None:
        await create_db_engine(state)

    return start_app


def get_stop_app_handler():
    async def stop_app(state: State) -> None:
        await dispose_db_engine(state)

    return stop_app
