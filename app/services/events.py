"""
app.services.events
~~~~~~~~~~~~~~~~~~~

This module contains functions that the ASGI server will invoke on on_startup &
on_shutdown events.
"""
import aiohttp
import starlite

from app.core.config import settings
from app.services import object_processor


async def create_object_processor_client(state: starlite.State) -> None:
    state.object_processor = object_processor.ObjectProcessor(
        settings.certinize_object_processor
    )
    state.object_processor_session = state.object_processor.session


async def dispose_client_sessions(state: starlite.State) -> None:
    if isinstance(state.object_processor_session, aiohttp.ClientSession):
        await state.object_processor_session.close()
