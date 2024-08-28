from starlette.middleware.base import BaseHTTPMiddleware

from .continue_dev import continue_dev_middleware
from .default import default_middleware
from .langfuse import langfuse_middleware
from .ollama import ollama_middleware

MIDDLEWARES = {
    BaseHTTPMiddleware: [
        langfuse_middleware,
        ollama_middleware,
        continue_dev_middleware,
        default_middleware,
    ]
}
