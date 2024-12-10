from . import continue_dev, ollama, server, user

routers = [
    user.router,
    ollama.router,
    server.router,
    continue_dev.router,
]

__all__ = ["routers"]
