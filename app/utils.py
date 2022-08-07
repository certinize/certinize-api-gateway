import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Coroutine

from nacl.bindings import crypto_core
from solana import publickey

from app.core import exceptions


class Utils:
    def exec_async(
        self,
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

    async def wallet_address_must_be_on_curve(self, wallet_address: str) -> str:
        try:
            valid_point = crypto_core.crypto_core_ed25519_is_valid_point(
                bytes(publickey.PublicKey(wallet_address))
            )
        except ValueError as val_err:
            err = (
                str(val_err)
                .replace("'", "")
                .replace("(", "")
                .replace(")", "")
                .replace(",", "")
            )
            raise ValueError(err) from val_err

        if not valid_point:
            raise exceptions.OnCurveException("the point must be on the curve")

        return wallet_address
