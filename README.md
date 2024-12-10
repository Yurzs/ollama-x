# Ollama-X

Ollama-X is a proxy server with extensions for the Ollama API. It provides additional functionality and features to enhance the capabilities of the Ollama API.

## Project Description

Ollama-X is designed to extend the functionality of the Ollama API by providing additional features and capabilities. It acts as a proxy server, allowing you to interact with the Ollama API while adding custom extensions and enhancements.

This project allows load balancing between Ollama instances, adds login/password authentication, and integrates with the continue.dev plugin, adding remote config availability.

## Setup

Follow the instructions below to set up the project.

### Prerequisites

- Docker
- Docker Compose
- Make

### Building and Running Docker Containers

1. Clone the repository:

   ```sh
   git clone https://github.com/Yurzs/ollama-x.git
   cd ollama-x
   ```

2. Build and run the Docker containers using `docker-compose`:

   ```sh
   docker-compose up --build
   ```

3. The application will be available at `http://localhost:8000`.
