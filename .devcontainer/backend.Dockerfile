FROM mcr.microsoft.com/devcontainers/python:3.12

# Install the required packages
RUN apt update && apt install gcc musl-dev

# Install dependencies
RUN pip install "poetry>=1,<2"

WORKDIR /workspace

# Copy the poetry.lock and pyproject.toml files
COPY pyproject.toml poetry.toml ./

# Copy the rest of the files
COPY ollama_x ollama_x
COPY README.md .

# Install the dependencies
RUN poetry install

ENTRYPOINT ["poetry", "run"]
