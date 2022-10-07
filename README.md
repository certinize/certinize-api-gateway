# certinize-api-gateway

![repo-size](https://img.shields.io/github/repo-size/certinize/certinize-api-gateway)
![lines-of-code](https://img.shields.io/tokei/lines/github.com/certinize/certinize-api-gateway)
![python-version](https://img.shields.io/badge/python-v3.10-blue)
![build-check](https://img.shields.io/github/workflow/status/certinize/certinize-api-gateway/Python%20application)
![license](https://img.shields.io/github/license/certinize/certinize-api-gateway)

## Test

The mock server is available on Postman:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://god.gw.postman.com/run-collection/14719803-c7929fed-c243-4a04-8076-53d35aaa8468?action=collection%2Ffork&collection-url=entityId%3D14719803-c7929fed-c243-4a04-8076-53d35aaa8468%26entityType%3Dcollection%26workspaceId%3D4cb1727d-8f73-4063-8bc1-af86b4222d4e)

## Installation

Fork the [certinize-api-gateway](https://github.com/certinize/certinize-api-gateway) repo on GitHub, then [clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository) your fork locally.

## Setup

1. `cd` into the project directory, e.g., certinize-api-gateway.

2. Inside the project's root directory, run `poetry shell`. This will create or start the virtual environment. Make sure [poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) is installed.

3. Run `poetry install`. This will install the project and its dependencies.

4. Create a copy of `.env.example`:

    ```sh
    cp .env.example .env
    ```

5. Run the app: `uvicorn app.main:app`.

6. Go to `http://127.0.0.1:8000/schema`.

## Contributing

Check the [contributing guide](https://github.com/certinize/certinize-api-gateway/blob/main/.github/CONTRIBUTING.md) to learn more about the development process and how you can test your changes.
