# zaique

## Installation

Fork the [zaique](https://github.com/certinize/zaique) repo on GitHub, then [clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository#cloning-a-repository) your fork locally.

## Setup

1. `cd` into the project directory, e.g., zaique.

2. Inside the project's root directory, run `poetry shell`. This will create or start the virtual environment. Make sure [poetry](https://python-poetry.org/docs/master/#installing-with-the-official-installer) is installed.

3. Run `poetry install`. This will install the project and its dependencies.

4. Create a copy of `.env.example`:

    ```sh
    cp .env.example .env
    ```

5. Run the app: `uvicorn app.main:app`.

6. Go to `http://127.0.0.1:8000/schema`.
