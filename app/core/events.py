from starlite import State

from app.db import events as db_events
from app.services import events as svcs_events


def get_start_app_handler():
    async def start_app(state: State) -> None:
        await db_events.create_db_engine(state)
        await db_events.create_db_tables(state)
        await svcs_events.create_image_processor_client(state)

    return start_app


def get_stop_app_handler():
    async def stop_app(state: State) -> None:
        await db_events.dispose_db_engine(state)
        await svcs_events.dispose_client_sessions(state)

    return stop_app
