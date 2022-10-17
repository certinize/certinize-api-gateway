import asyncio
import typing
from concurrent import futures

import aiohttp
import orjson
from nacl.bindings import crypto_core
from solana import publickey


def exec_async(
    function: typing.Callable[[typing.Any], typing.Any]
    | typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, str]],
    *args: typing.Any,
    **kwargs: typing.Any
) -> typing.Any:
    """Asynchronously run sync functions or methods outside an event loop.

    Args:
        fn (Callable[..., Coroutine[typing.Any, typing.Any, str]]): The sync method to
            be run asynchronously.

    Returns:
        typing.Any: Return value(s) of the sync method.
    """
    return (
        futures.ThreadPoolExecutor(1)
        .submit(asyncio.run, function(*args, **kwargs))
        .result()
    )


def create_http_client(
    headers: dict[str, str], endpoint_url: str
) -> aiohttp.ClientSession:
    """Create an HTTP client session.

    Args:
        headers (dict[str, str]): The headers to be used by the client session.
        endpoint_url (str): The base URL for the client session.

    Returns:
        aiohttp.ClientSession: The client session.
    """
    return aiohttp.ClientSession(
        headers=headers,
        base_url=endpoint_url,
        json_serialize=lambda json_: orjson.dumps(  # pylint: disable=E1101
            json_
        ).decode(),
    )


def pubkey_on_curve(value: str):
    """Validate that the issuer's public key is on the curve.

    Args:
        value (str): The issuer's public key.

    Raises:
        ValueError: If the public key is not on the curve.

    Returns:
        str: The issuer's public key.
    """
    try:
        crypto_core.crypto_core_ed25519_is_valid_point(
            bytes(publickey.PublicKey(value))
        )
    except ValueError as val_err:
        val_err.args = ("the point must be on the curve",)
        raise val_err from val_err

    return value
