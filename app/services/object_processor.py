"""
app.services.object_processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This modiles contains a client for interacting with certnize-ecert-processor's REST API.
"""
import typing

import aiohttp

from app import utils

CERTIFICATES = "/certificates"
TEMPLATES = "/templates"


class ObjectProcessor:
    """A client implementation of certinize-object-processor."""

    endpoint_url = ""
    headers: dict[str, str] = {}
    session: aiohttp.ClientSession

    def __init__(self, endpoint_url: str) -> None:
        self.endpoint_url = endpoint_url
        self._create_client_session()

    def _create_request_header(self) -> None:
        """Create default headers for the client session."""
        raise NotImplementedError

    def _create_client_session(self) -> None:
        """Initialize the client session."""
        self.session = utils.create_http_client(self.headers, self.endpoint_url)

    async def create_folder(
        self, folder_name: str, parent_folder_path: str
    ) -> dict[str, typing.Any]:
        """Create a folder on a cloud storage.

        Args:
            folder_name (str): Name of the folder.
            parent_folder_path (str): Path of the parent folder.

        Raises:
            ConnectionError: If the gateway failed to receive a valid response from
                `certinize-object-processor`.

        Returns:
            dict[str, typing.Any]: Decoded JSON object containing the result of the
                folder creation.
        """
        request_body = {
            "folderName": folder_name,
            "parentFolderPath": parent_folder_path,
        }

        try:
            response = await self.session.post(url=TEMPLATES, json=request_body)
        except aiohttp.ClientConnectorError as err:
            raise ConnectionError(str(err)) from err

        return await response.json()

    async def upload_object(
        self,
        objectb: str,
        object_name: str,
        options: dict[str, str],
    ) -> dict[str, typing.Any]:
        """Upload object file to a cloud storage.

        Args:
            objectb (bytes | typing.BinaryIO): The object content.
            object_name (str): Name of the object file.
            options (str): Other options. Refer to certinize-object-processor's docs
                regarding other options.

        Raises:
            ConnectionError: If the gateway failed to receive a valid response from
                `certinize-object-processor`.

        Returns:
            dict[str, typing.Any]: Decoded JSON object containing the result of the
                upload.
        """
        try:
            response = await self.session.post(
                url=TEMPLATES,
                json={
                    "filename": object_name,
                    "options": options,
                    "fileb": objectb,
                },
            )
        except aiohttp.ClientConnectorError as err:
            raise ConnectionError(str(err)) from err

        return await response.json()

    async def generate_certificate(
        self, certificate_meta: dict[str, typing.Any]
    ) -> tuple[dict[str, typing.Any], int]:
        try:
            response = await self.session.post(url=CERTIFICATES, json=certificate_meta)
        except aiohttp.ClientConnectionError as err:
            raise ConnectionError(str(err)) from err

        return (await response.json(), response.status)
