from starlite import State

from app.db import events as db_events
from app.services import events as scvs_events


def get_start_app_handler():
    async def start_app(state: State) -> None:
        await db_events.create_db_engine(state)
        await db_events.create_db_tables(state)
        await scvs_events.create_s3_client(state)

    return start_app


def get_stop_app_handler():
    async def stop_app(state: State) -> None:
        await db_events.dispose_db_engine(state)
        await scvs_events.create_s3_client(state)

    return stop_app
