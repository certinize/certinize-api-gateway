"""
app.services.image_processor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This modiles contains a client for interacting with certnize-ecert-processor's REST API.
"""
import typing

import aiohttp
import orjson

CERTIFICATES = "/certificates"
TEMPLATES = "/templates"


class ImageProcessor:
    """A client implementation of certinize-image-processor."""

    endpoint_url = ""
    headers: dict[str, typing.Any] = {}
    session: aiohttp.ClientSession

    def __init__(self, endpoint_url: str) -> None:
        self.endpoint_url = endpoint_url
        self._create_client_session()

    def _create_request_header(self) -> None:
        """Create default headers for the client session."""
        raise NotImplementedError

    def _create_client_session(self) -> None:
        """Initialize the client session."""
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            base_url=self.endpoint_url,
            json_serialize=lambda json_: orjson.dumps(  # pylint: disable=E1101
                json_
            ).decode(),
        )

    async def create_folder(
        self, folder_name: str, parent_folder_path: str
    ) -> dict[str, typing.Any]:
        """Create a folder on a cloud storage.

        Args:
            folder_name (str): Name of the folder.
            parent_folder_path (str): Path of the parent folder.

        Raises:
            ConnectionError: If the gateway failed to receive a valid response from
                `certinize-ecert-processor`.

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

    async def upload_file(
        self,
        imageb: bytes | typing.BinaryIO,
        image_name: str,
        options: str,
    ) -> dict[str, typing.Any]:
        """Upload image file to a cloud storage.

        Args:
            imageb (bytes | typing.BinaryIO): The image content.
            image_name (str): Name of the image file.
            options (str): Other options. Refer to certinize-ecert-processor's docs
                regarding other options.

        Raises:
            ConnectionError: If the gateway failed to receive a valid response from
                `certinize-ecert-processor`.

        Returns:
            dict[str, typing.Any]: Decoded JSON object containing the result of the
                upload.
        """
        form_data = aiohttp.FormData()
        form_data.add_field("filename", image_name)
        form_data.add_field("options", options)
        form_data.add_field("fileb", imageb)

        try:
            response = await self.session.post(url=TEMPLATES, data=form_data)
        except aiohttp.ClientConnectorError as err:
            raise ConnectionError(str(err)) from err

        return await response.json()
