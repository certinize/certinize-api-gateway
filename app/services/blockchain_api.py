"""
app.services.blockchain_api
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains utilities for interacting with Certinize's blockchain API service.
"""
import typing

import aiohttp

from app import utils

ISSUANCES = "/issuances"


class BlockchainInterface:  # pylint: disable=too-few-public-methods
    """A client implementation of certinize-blockchain-api"""

    endpoint_url = ""
    headers: dict[str, str] = {}
    session: aiohttp.ClientSession

    def __init__(self, endpoint_url: str) -> None:
        assert isinstance(endpoint_url, str)
        self.endpoint_url = endpoint_url
        self._init_http_client()

    def _init_request_header(self) -> None:
        """Initialize the default headers for the client session."""
        raise NotImplementedError

    def _init_http_client(self) -> None:
        """Initialize the client session."""
        self.session = utils.create_http_client(self.headers, self.endpoint_url)

    async def issue_certificate(
        self, issuance_request: typing.Any
    ) -> tuple[typing.Any, int]:
        """Issue a certificate to a recipient."""
        async with self.session.post(
            url=ISSUANCES, json=issuance_request.dict()
        ) as response:
            return (await response.json(), response.status)
