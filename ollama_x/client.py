import aiohttp
from pydantic import HttpUrl


class OllamaClient:
    """Client to Ollama Server API."""

    def __init__(self, base_url: str | HttpUrl):
        self.base_url = str(base_url)

    async def send_request(self, path: str, method: str, **kwargs) -> aiohttp.ClientResponse:
        """Send request to the server."""

        async with aiohttp.ClientSession(self.base_url) as session:
            async with getattr(session, method)(path, **kwargs) as response:
                await response.read()
                return response

    async def list_models(self) -> aiohttp.ClientResponse:
        """List all models available on the server."""

        return await self.send_request("/api/tags", "get")

    async def show_model_info(self, model_name: str) -> aiohttp.ClientResponse:
        """Show model information."""

        return await self.send_request(f"/api/show", "post", json={"name": model_name})

    async def list_running_models(self) -> aiohttp.ClientResponse:
        """List all running models."""

        return await self.send_request("/api/ps", "get")
