import starlite

from app.services import blockchain_api, object_processor


def get_object_processor_client(
    state: starlite.State,
) -> object_processor.ObjectProcessor:
    return state.object_processor


def get_blockchain_api_client(
    state: starlite.State,
) -> blockchain_api.BlockchainInterface:
    return state.blockchain_api
