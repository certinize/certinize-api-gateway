import starlite
from types_aiobotocore_s3 import client


async def get_s3_client(state: starlite.State) -> client.S3Client:
    return state.s3_client
