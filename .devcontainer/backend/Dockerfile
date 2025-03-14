FROM mcr.microsoft.com/devcontainers/python:3.12

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    zsh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install poetry
RUN pip install "poetry>1,<2"

# Set shell for devcontainer
SHELL ["/bin/bash", "-c"]
