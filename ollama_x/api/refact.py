from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from ollama_x import types
from ollama_x.api import endpoints
from ollama_x.api.ollama import get_models, get_running_models
from ollama_x.config import config
from ollama_x.model import OllamaModel
from ollama_x.model.refact import ModelRecord, RefactCodeAssistantCaps

router = APIRouter(tags=["refact"])


async def get_caps(models):
    """Get refact code assistant capabilities."""

    return RefactCodeAssistantCaps(
        cloud_name="OllamaX",
        endpoint_template=endpoints.OPENAI_CHAT_COMPLETIONS,
        endpoint_chat_passthrough=endpoints.OPENAI_CHAT,
        endpoint_style="openai",
        tokenizer_path_template="/openai/v1/model/$MODEL/tokenizer.json",
        code_completion_default_model=config.default_completions_model,
        code_completion_n_ctx=2048,
        code_chat_default_model=config.default_chat_model,
        telemetry_basic_dest=endpoints.REFACT_TELEMETRY_BASIC,
        telemetry_corrected_snippets_dest=endpoints.REFACT_TELEMETRY_CORRECTED_SNIPPETS,
        default_embeddings_model=config.default_embeddings_model,
        endpoint_embeddings_template=endpoints.OPENAI_EMBEDDINGS,
        endpoint_embeddings_style="openai",
        size_embeddings=768,
        running_models=[
            types.OllamaModel(name) >> types.OpenAIModel for name in await get_running_models()
        ],
        code_chat_models=await get_models_info(list(models)),
        code_completion_models=await get_models_info(list(models)),
        customization="",
    )


async def get_models_info(models: list[str]) -> dict[str, ModelRecord]:
    """Get models info."""

    return {
        types.OllamaModel(model.id) >> types.OpenAIModel: ModelRecord.from_model(model)
        async for model in OllamaModel.all(models)
    }


@router.get(
    endpoints.REFACT_CAPS,
    response_model=RefactCodeAssistantCaps,
    response_model_exclude_none=True,
)
async def refact_caps(request: Request):
    """Get refact code assistant capabilities."""

    models = await get_models()

    return await get_caps(models)


@router.post(endpoints.REFACT_CODING_ASSISTANT)
async def refact_code_assistant_caps_json(request: Request) -> JSONResponse:
    """Get refact code assistant capabilities."""

    models = await get_models()

    caps = await get_caps(models)

    return JSONResponse(caps.model_dump(mode="json", exclude_none=True))


@router.post(endpoints.REFACT_TELEMETRY_BASIC)
async def refact_telemetry_basic(request: Request):
    raise NotImplementedError()


@router.post(endpoints.REFACT_TELEMETRY_CORRECTED_SNIPPETS)
async def refact_telemetry_feedback(request: Request):
    raise NotImplementedError()
