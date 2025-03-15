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
- Python 3.12+
- uv (install with `pip install uv`)

### Local Development Setup

1. Clone the repository:
   ```sh
   git clone https://github.com/Yurzs/ollama-x.git
   cd ollama-x
   ```

2. Create a virtual environment and install dependencies:
   ```sh
   make setup
   ```

3. Format code and run linters:
   ```sh
   make format
   ```

### Building and Running Docker Containers

1. Build and run the Docker containers:
   ```sh
   docker-compose up --build
   ```

2. The application will be available at `http://localhost:8000`.

## Environment Variables

The following environment variables are used to configure the services in this project:

- `MONGO_URI`: The URI for connecting to the MongoDB instance. Example: `mongodb://mongo:27017`
- `LANGFUSE_HOST`: The host for the Langfuse service.
- `LANGFUSE_PUBLIC_KEY`: The public key for the Langfuse service.
- `LANGFUSE_SECRET_KEY`: The secret key for the Langfuse service.
- `ENFORCE_MODEL`: The model to enforce for all requests.
- `USER_REGISTRATION_ENABLED`: Flag to enable or disable user registration.
- `SENTRY_DSN`: The DSN for Sentry error tracking.
- `ANONYMOUS_ALLOWED`: Flag to allow or disallow anonymous access.
- `ANONYMOUS_MODEL`: The model to enforce for anonymous users.
- `DOMAIN_NAME`: The domain name for the application.
