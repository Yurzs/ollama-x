from .continue_dev import router as continue_dev_router
from .proxy import router as proxy_router
from .server import router as server_router
from .user import router as user_router

routers = [user_router, proxy_router, server_router, continue_dev_router]

__all__ = ["routers"]
