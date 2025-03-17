from fastapi import FastAPI
from fastapi.routing import APIRoute

from ollama_x.api import exceptions, routers
from ollama_x.api.middleware import MIDDLEWARES
from ollama_x.startup import setup_log, setup_document, setup_sentry, ensure_indexes

app = FastAPI(
    on_startup=[
        setup_log,
        setup_document,
        ensure_indexes,
        setup_sentry,
    ],
    title="Ollama X",
    description="Ollama X API",
    version="1.0.0",
    root_path="/api",
)

for router in routers:
    app.include_router(router)

for exc, handler in exceptions.HANDLERS.items():
    app.add_exception_handler(exc, handler)


for mw_type, middlewares in MIDDLEWARES.items():
    for middleware in middlewares:
        app.add_middleware(mw_type, dispatch=middleware)


def use_route_names_as_operation_ids(fapp: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """

    for route in fapp.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


use_route_names_as_operation_ids(app)
