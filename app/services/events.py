"""
app.services.events
~~~~~~~~~~~~~~~~~~~

This module contains functions that the ASGI server will invoke on on_startup &
on_shutdown events.
"""
import contextlib

import aiohttp
import starlite
from aiobotocore import session

from app.core.config import settings
from app.services import filebase, image_processor


async def create_image_processor_client(state: starlite.State) -> None:
    state.image_processor = image_processor.ImageProcessor(
        settings.certinize_image_processor
    )
    state.image_processor_session = state.image_processor.session


async def create_s3_client(state: starlite.State) -> None:
    """Create an S3 client using an external exit stack.

    Args:
        state (starlite.State): An object that can be used to store arbitrary state.
    """
    state.filebase_client = filebase.FilebaseClient()
    state.s3_client_exit_stack = contextlib.AsyncExitStack()
    state.s3_client = await state.s3_client_exit_stack.enter_async_context(
        session.AioSession().create_client(  # type: ignore
            "s3",
            endpoint_url=settings.s3_api_endpoint_url,
            aws_secret_access_key=settings.s3_secret_access_key,
            aws_access_key_id=settings.s3_access_key_id,
        )
    )


async def dispose_s3_client(state: starlite.State) -> None:
    """Exit the S3 client's runtime context.

    Args:
        state (starlite.State): An object that can be used to store arbitrary state.
    """
    if isinstance(state.s3_client_exit_stack, contextlib.AsyncExitStack):
        await state.s3_client_exit_stack.aclose()


async def dispose_client_sessions(state: starlite.State) -> None:
    if isinstance(state.image_processor_session, aiohttp.ClientSession):
        await state.image_processor_session.close()
