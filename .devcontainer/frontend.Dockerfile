FROM mcr.microsoft.com/devcontainers/javascript-node:0-18

# Install additional tools if needed
RUN apt-get update && apt-get -y install git
