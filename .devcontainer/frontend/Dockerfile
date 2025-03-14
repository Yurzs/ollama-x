FROM mcr.microsoft.com/devcontainers/javascript-node:latest

# Create nonroot user and group
RUN groupadd -g 1001 nonroot && \
    useradd -u 1001 -g nonroot -m -s /usr/bin/zsh nonroot

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    zsh \
    && rm -rf /var/lib/apt/lists/*

# Set zsh as default shell
RUN chsh -s /usr/bin/zsh nonroot

# Switch to non-root user for the rest of the setup
USER nonroot

# Set the working directory
WORKDIR /app

ENV PATH="/home/nonroot/.local/bin:${PATH}"
CMD [ "sleep", "infinity" ]
