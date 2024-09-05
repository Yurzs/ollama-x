import ssl
from contextlib import asynccontextmanager
from typing import Any

import aiohttp
import certifi
from aiohttp import TCPConnector
from pydantic import HttpUrl


class OllamaClient:
    """Client to Ollama Server API."""

    def __init__(self, base_url: str | HttpUrl | None, is_self: bool = False):
        self.base_url = str(base_url) if base_url is not None else None
        self.is_self = is_self

    @asynccontextmanager
    async def send_request(
        self,
        path: str,
        method: str,
        base_url: None | str = None,
        **kwargs,
    ) -> aiohttp.ClientResponse:
        """Send request to the server."""

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        if self.base_url is None and base_url is None:
            raise RuntimeError("Base url is not provided.")

        async with aiohttp.ClientSession(
            base_url or self.base_url, connector=TCPConnector(ssl=ssl_context)
        ) as session:
            async with getattr(session, method)(path, timeout=5, **kwargs) as response:
                yield response

    def list_models(self) -> aiohttp.ClientResponse:
        """List all models available on the server."""

        return self.send_request("/api/tags", "get")

    def show_model_info(self, model_name: str, verbose=False) -> aiohttp.ClientResponse:
        """Show model information."""

        return self.send_request(
            "/api/show",
            "post",
            json={
                "name": model_name,
                "verbose": verbose,
            },
        )

    def list_running_models(self) -> aiohttp.ClientResponse:
        """List all running models."""

        return self.send_request("/api/ps", "get")

    async def tokenize(self, model_name: str, prompt: str) -> aiohttp.ClientResponse:
        return self.send_request(
            "/api/tokenize",
            "post",
            json={
                "model": model_name,
                "prompt": prompt,
            },
        )

    @classmethod
    def get_model_params(cls, model_name: str) -> tuple[str, str]:
        version = "latest"

        if "/" not in model_name:
            model_name = f"library/{model_name}"

        if ":" in model_name:
            model_name, version = model_name.split(":", 1)

        return model_name, version

    async def get_manifest(self, model_name: str):
        model_name, version = self.get_model_params(model_name)

        return await self.send_request(
            f"/v2/{model_name}/manifests/{version}",
            "get",
            base_url="https://registry.ollama.ai",
        )

    async def download_blob(self, model_name: str, digest: str) -> aiohttp.ClientResponse:
        model_name, _ = self.get_model_params(model_name)

        return await self.send_request(
            f"/v2/{model_name}/blobs/{digest}",
            "get",
            base_url="https://registry.ollama.ai",
        )

    def chat(
        self,
        request: dict[str, Any],
        headers: dict[str, Any],
    ) -> aiohttp.ClientResponse:
        return self.send_request(
            "/api/chat",
            "post",
            json=request,
            headers=headers,
        )
