import ssl
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncGenerator, Union

import aiohttp
import certifi
from aiohttp import ClientTimeout, TCPConnector
from pydantic import HttpUrl
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from typing_extensions import TypeVar


R = TypeVar("R")


class OllamaModelDetails(BaseModel):
    format: str
    family: str
    families: Optional[Union[str, List[str]]]
    parameter_size: str
    quantization_level: str


class OllamaModel(BaseModel):
    name: str
    modified_at: datetime
    size: int
    digest: str
    details: OllamaModelDetails


class OllamaModelInfo(BaseModel):
    general_architecture: str
    general_file_type: int
    general_parameter_count: int
    general_quantization_version: int
    llama_attention_head_count: int
    llama_attention_head_count_kv: int
    llama_attention_layer_norm_rms_epsilon: float
    llama_block_count: int
    llama_context_length: int
    llama_embedding_length: int
    llama_feed_forward_length: int
    llama_rope_dimension_count: int
    llama_rope_freq_base: int
    llama_vocab_size: int
    tokenizer_ggml_bos_token_id: int
    tokenizer_ggml_eos_token_id: int
    tokenizer_ggml_merges: List[Any]
    tokenizer_ggml_model: str
    tokenizer_ggml_pre: str
    tokenizer_ggml_token_type: List[Any]
    tokenizer_ggml_tokens: List[Any]


class OllamaListModelsResponse(BaseModel):
    models: List[OllamaModel]


class OllamaModelShowResponse(BaseModel):
    modelfile: str
    parameters: str
    template: str
    details: OllamaModelDetails
    model_info: OllamaModelInfo


class OllamaPullModelRequest(BaseModel):
    model: str
    insecure: Optional[bool] = False
    stream: Optional[bool] = True


class OllamaPullModelResponseStream(BaseModel):
    status: str
    digest: Optional[str] = None
    total: Optional[int] = None
    completed: Optional[int] = None


class OllamaPullModelResponseSingle(BaseModel):
    status: str


class OllamaRunningModel(BaseModel):
    name: str
    model: str
    size: int
    digest: str
    details: OllamaModelDetails
    expires_at: datetime
    size_vram: int


class OllamaListRunningModelsResponse(BaseModel):
    models: List[OllamaRunningModel]


class OllamaClient:
    """Client to Ollama Server API."""

    def __init__(self, base_url: str | HttpUrl | None, is_self: bool = False):
        self.base_url = str(base_url) if base_url is not None else None
        self.is_self = is_self

    async def stream_request(
        self,
        path: str,
        method: str,
        response_model: R,
        base_url: None | str = None,
        **kwargs,
    ):
        """Handle streaming response from the server."""

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        if self.base_url is None and base_url is None:
            raise RuntimeError("Base url is not provided.")

        async with aiohttp.ClientSession(
            base_url or self.base_url,
            connector=TCPConnector(ssl=ssl_context),
        ) as session:
            async with getattr(session, method)(path, timeout=5 * 60, **kwargs) as response:
                if response.status != 200:
                    raise Exception("Failed to connect to the server.")

                async for chunk in response.content:
                    data = response_model.model_validate_json(chunk).model_dump_json(
                        by_alias=True, exclude_none=True
                    )
                    yield f"{data}\n"

    @asynccontextmanager
    async def send_request(
        self,
        path: str,
        method: str,
        response_model: R,
        base_url: None | str = None,
        **kwargs,
    ) -> AsyncGenerator[Union[R, AsyncGenerator[R, None]], None]:
        """Send request to the server."""

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        if self.base_url is None and base_url is None:
            raise RuntimeError("Base url is not provided.")

        async with aiohttp.ClientSession(
            base_url or self.base_url, connector=TCPConnector(ssl=ssl_context)
        ) as session:
            async with getattr(session, method)(path, timeout=5, **kwargs) as response:
                if response.status != 200:
                    raise Exception("Failed to connect to the server.")

                if response_model is None:
                    yield None
                else:
                    yield response_model.model_validate(await response.json())

    def list_models(self) -> AsyncContextManager[OllamaListModelsResponse]:
        """List all models available on the server."""

        return self.send_request("/api/tags", "get", response_model=OllamaListModelsResponse)

    def show_model_info(
        self, model_name: str, verbose=False
    ) -> AsyncContextManager[OllamaModelShowResponse]:
        """Show model information."""

        return self.send_request(
            "/api/show",
            "post",
            json={
                "name": model_name,
                "verbose": verbose,
            },
            response_model=OllamaModelShowResponse,
        )

    def list_running_models(self) -> AsyncContextManager[OllamaListRunningModelsResponse]:
        """List all running models."""

        return self.send_request("/api/ps", "get", response_model=OllamaListRunningModelsResponse)

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

    def get_manifest(self, model_name: str):
        model_name, version = self.get_model_params(model_name)

        return self.send_request(
            f"/v2/{model_name}/manifests/{version}",
            "get",
            base_url="https://registry.ollama.ai",
        )

    def pull_model(
        self,
        model_name: str,
        stream: bool = True,
    ) -> AsyncContextManager[Union[OllamaPullModelResponseSingle, OllamaPullModelResponseStream]]:
        """Pull model to the server."""

        method = self.send_request if not stream else self.stream_request

        return method(
            "/api/pull",
            "post",
            json=OllamaPullModelRequest(
                model=model_name,
                insecure=self.is_self,
                stream=stream,
            ).model_dump(mode="json", by_alias=True, exclude_none=True),
            response_model=OllamaPullModelResponseSingle
            if not stream
            else OllamaPullModelResponseStream,
        )

    def delete_model(self, model_name: str) -> AsyncContextManager[None]:
        """Delete model from the server."""

        return self.send_request(
            "/api/delete",
            "delete",
            json={"name": model_name},
            response_model=None,
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
