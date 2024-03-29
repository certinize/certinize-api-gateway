from starlite import State

from app.db import events as db_events
from app.services import events as svcs_events


def get_start_app_handler():
    async def start_app(state: State) -> None:
        await db_events.create_db_engine(state)
        await db_events.create_db_tables(state)
        await svcs_events.create_object_processor_client(state)
        await svcs_events.create_blockchain_api_client(state)

    return start_app


def get_stop_app_handler():
    async def stop_app(state: State) -> None:
        await db_events.dispose_db_engine(state)
        await svcs_events.dispose_object_processor_sessions(state)
        await svcs_events.dispose_blockchain_api_sessions(state)

    return stop_app
