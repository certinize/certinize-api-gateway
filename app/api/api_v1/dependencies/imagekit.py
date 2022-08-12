import starlite

from app.services import imagekit


async def get_imagekit_client(state: starlite.State) -> imagekit.ImageKitClient:
    return state.imagekit_client
