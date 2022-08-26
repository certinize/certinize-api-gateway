import asyncio
import typing
from concurrent import futures


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
