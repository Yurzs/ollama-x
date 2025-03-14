FROM mcr.microsoft.com/devcontainers/python:3.12

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    zsh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv
RUN pip install uv

# Set shell for devcontainer
SHELL ["/bin/bash", "-c"]

# Create a symlink for bash to ensure scripts work correctly
RUN ln -s /bin/bash /usr/bin/bash
