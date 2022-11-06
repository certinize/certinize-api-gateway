import asyncio
import base64
import binascii
import enum
import re
import typing
from concurrent import futures

import aiohttp
import orjson
import pydantic
import solders.keypair as solders_keypair  # type: ignore # pylint: disable=E0401
import starlite
from nacl.bindings import crypto_core
from solana import publickey
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import engine

from app.core import abc
from app.models.schemas import users

PANIC_EXC = re.compile(r"\((.*?)\)")
INVALID_CHAR = re.compile(r"(?<=: ).*(?=\s{)")


class RustError(enum.Enum):
    INVALIDCHARACTER = "found unsupported characters"


def exec_async(
    function: typing.Callable[[typing.Any], typing.Any]
    | typing.Callable[..., typing.Coroutine[typing.Any, typing.Any, str]],
    *args: typing.Any,
    **kwargs: typing.Any,
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


def raise_rust_error(error: BaseException) -> None:
    try:
        raise ValueError(PANIC_EXC.findall(str(error))[1]) from error
    except IndexError:
        raise ValueError(
            RustError[INVALID_CHAR.findall(str(error))[0].upper()].value
        ) from error


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


def pvtkey_on_curve(value: str):
    """Validate that the issuer's private key is on the curve.

    Args:
        value (str): The issuer's private key.

    Raises:
        ValueError: If the private key is not on the curve.

    Returns:
        str: The issuer's private key.
    """
    try:
        solders_keypair.Keypair().from_base58_string(value)
    except BaseException as base_err:  # pylint: disable=W0703
        raise_rust_error(base_err)

    return value


def image_is_valid_base64(value: str):
    """Validate that the image is a valid base64 string.

    Args:
        value (str): The base64 encoded image.

    Raises:
        ValueError: If the image is not a valid base64 string.

    Returns:
        str: The base64 encoded image.
    """
    try:
        base64.b64decode(value, validate=True)
    except binascii.Error as error:
        raise ValueError("image is not a valid base64 string") from error

    return value


async def check_api_key_exists(
    database: abc.Database,
    db_engine: engine.AsyncEngine,
    token: str,
    /,
) -> None:
    user = users.SolanaUsers(
        api_key=pydantic.UUID5(token),
    )

    try:
        result = await database.select(db_engine, user, "api_key", token)
        result.one()
    except exc.NoResultFound as no_result:
        raise starlite.HTTPException(
            status_code=401,
            detail=f"User not found: {token}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        ) from no_result
