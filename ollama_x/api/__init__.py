from . import continue_dev, proxy, server, user

routers = [user.router, proxy.router, server.router, continue_dev.router]

__all__ = ["routers"]
