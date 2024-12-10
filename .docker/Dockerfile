FROM python:3.12-alpine

# Install the required packages
RUN apk add --no-cache gcc musl-dev linux-headers

# Install dependencies
RUN pip install poetry

WORKDIR /app

# Copy the poetry.lock and pyproject.toml files
COPY pyproject.toml poetry.toml ./

# Copy the rest of the files
COPY ollama_x ollama_x
COPY README.md .

# Install the dependencies
RUN poetry install

ENTRYPOINT ["poetry", "run"]

CMD ["python", "-m", "uvicorn", "ollama_x.app:app", "--host", "0.0.0.0"]
