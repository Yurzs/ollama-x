from . import continue_dev, ollama, openai, refact, server, user

routers = [
    user.router,
    ollama.router,
    server.router,
    continue_dev.router,
    refact.router,
    openai.router,
]

__all__ = ["routers"]
