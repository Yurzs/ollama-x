ARG debug=0

FROM python:3.12-slim AS builder

# Install the required packages
RUN apt update && apt install -y gcc musl-dev

# Install dependencies
RUN pip install "poetry>1,<2"

WORKDIR /app

# Copy the poetry.lock and pyproject.toml files
COPY pyproject.toml ./

# Create a poetry.toml file to configure the virtual environment
RUN echo '[virtualenvs]\ncreate = true\nin-project = true\npath = ".venv"' > poetry.toml

# Copy the rest of the files
COPY ollama_x ollama_x
COPY README.md .

# Install the dependencies
RUN poetry install

FROM gcr.io/distroless/python3-debian12:${debug:+debug-}nonroot

COPY --from=builder /app /app
COPY --from=builder /usr/local/lib /usr/local/lib
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /etc/ld.so.cache /etc/ld.so.cache

WORKDIR /app

ENV PATH="/app/.venv/bin:${PATH}"

ENTRYPOINT []

CMD ["uvicorn", "ollama_x.app:app", "--host", "0.0.0.0"]
