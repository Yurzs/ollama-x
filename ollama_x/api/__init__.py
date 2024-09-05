from . import continue_dev, openai, proxy, refact, server, user

routers = [
    user.router,
    proxy.router,
    server.router,
    continue_dev.router,
    refact.router,
    openai.router,
]

__all__ = ["routers"]
