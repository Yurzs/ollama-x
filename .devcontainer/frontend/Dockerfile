FROM mcr.microsoft.com/devcontainers/javascript-node:latest

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    zsh \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

CMD [ "sleep", "infinity" ]
