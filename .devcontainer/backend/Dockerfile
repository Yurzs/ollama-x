FROM mcr.microsoft.com/devcontainers/python:3.12

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

# Copy the entire project and install
COPY . .
RUN poetry install

# Set shell for devcontainer
SHELL ["/bin/bash", "-c"]