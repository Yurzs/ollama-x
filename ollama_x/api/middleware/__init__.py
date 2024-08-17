from starlette.middleware.base import BaseHTTPMiddleware

from .langfuse import langfuse_middleware
from .ollama import ollama_middleware

MIDDLEWARES = {BaseHTTPMiddleware: [langfuse_middleware, ollama_middleware]}
