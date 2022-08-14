import starlite

from app.services import image_processor


async def get_image_processor_client(
    state: starlite.State,
) -> image_processor.ImageProcessor:
    return state.image_processor
