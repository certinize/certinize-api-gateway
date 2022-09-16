import starlite

from app.services import object_processor


async def get_object_processor_client(
    state: starlite.State,
) -> object_processor.ObjectProcessor:
    return state.image_processor
