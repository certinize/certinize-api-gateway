import starlite
from types_aiobotocore_s3 import client

from app.services import filebase


async def get_s3_client(state: starlite.State) -> client.S3Client:
    return state.s3_client


async def get_filebase_client(state: starlite.State) -> filebase.FilebaseClient:
    return state.filebase_client
