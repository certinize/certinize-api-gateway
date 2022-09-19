"""
app.services.events
~~~~~~~~~~~~~~~~~~~

This module contains functions that the ASGI server will invoke on on_startup &
on_shutdown events.
"""
import aiohttp
import starlite

from app.core.config import settings
from app.services import blockchain_api, object_processor


async def create_object_processor_client(state: starlite.State) -> None:
    state.object_processor = object_processor.ObjectProcessor(
        settings.certinize_object_processor
    )
    state.object_processor_session = state.object_processor.session


async def dispose_object_processor_sessions(state: starlite.State) -> None:
    if isinstance(state.object_processor_session, aiohttp.ClientSession):
        await state.object_processor_session.close()


async def create_blockchain_api_client(state: starlite.State) -> None:
    state.blockchain_api = blockchain_api.BlockchainInterface(
        settings.certinize_blockchain_api
    )
    state.blockchain_api_session = state.blockchain_api.session


async def dispose_blockchain_api_sessions(state: starlite.State) -> None:
    if isinstance(state.blockchain_api_session, aiohttp.ClientSession):
        await state.blockchain_api_session.close()
