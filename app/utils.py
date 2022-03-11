import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Coroutine


def exec_async(
    fn: Callable[[Any], Any] | Callable[..., Coroutine[Any, Any, str]],
    *args: Any,
    **kwargs: Any
) -> Any:
    """Asynchronously run sync functions or methods outside an event loop.

    Args:
        fn (Callable[..., Coroutine[Any, Any, str]]): The sync method to be run
            asynchronously.

    Returns:
        Any: Return value(s) of the sync method.
    """
    return ThreadPoolExecutor(1).submit(asyncio.run, fn(*args, **kwargs)).result()
