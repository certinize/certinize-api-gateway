# certinize-client-database

## Installation

Fork the [certinize-client-database](https://github.com/certinize/certinize-client-database) repo on GitHub, then [clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository) your fork locally.

## Setup

1. `cd` into the project directory, e.g., certinize-client-database.

2. Inside the project's root directory, run `poetry shell`. This will create or start the virtual environment. Make sure [poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) is installed.

3. Run `poetry install`. This will install the project and its dependencies.

4. Create a copy of `.env.example`:

    ```sh
    cp .env.example .env
    ```

5. Run the app: `uvicorn app.main:app`.

6. Go to `http://127.0.0.1:8000/schema`.

## Contributing

Check the [contributing guide](https://github.com/certinize/certinize-client-database/blob/main/.github/CONTRIBUTING.md) to learn more about the development process and how you can test your changes.
