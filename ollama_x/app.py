from fastapi import FastAPI

import ollama_x.model
from ollama_x.api import exceptions, routers
from ollama_x.api.middleware import MIDDLEWARES
from ollama_x.config import config  # noqa

app = FastAPI()

for router in routers:
    app.include_router(router)

for exc, handler in exceptions.HANDLERS.items():
    app.add_exception_handler(exc, handler)


for mw_type, middlewares in MIDDLEWARES.items():
    for middleware in middlewares:
        app.add_middleware(mw_type, dispatch=middleware)
