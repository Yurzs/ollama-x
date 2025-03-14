ARG debug=0
FROM python:3.12-slim AS builder

# Install the required packages and uv
RUN apt update && apt install -y gcc musl-dev git \
    && pip install uv

WORKDIR /app

# Copy the project files
COPY pyproject.toml ./
COPY ollama_x ollama_x
COPY README.md .

# Create virtual environment and install dependencies
RUN uv venv .venv \
    && . .venv/bin/activate \
    && uv pip install -e .

FROM gcr.io/distroless/python3-debian12:${debug:+debug-}nonroot
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib /usr/local/lib
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /etc/ld.so.cache /etc/ld.so.cache
WORKDIR /app
ENV PATH="/app/.venv/bin:${PATH}"
ENTRYPOINT []
CMD ["uvicorn", "ollama_x.app:app", "--host", "0.0.0.0"]
