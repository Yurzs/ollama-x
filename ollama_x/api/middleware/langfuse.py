import asyncio
import logging
from typing import Callable, Coroutine

from fastapi import Request, Response
from langfuse.decorators import langfuse_context, observe
from pydantic import BaseModel, Field

from ollama_x.api.middleware.ollama import OllamaProxyMiddleware

LOG = logging.getLogger(__name__)


class LangfuseMiddleware(BaseModel):

    ollama: OllamaProxyMiddleware | None = Field(None, description="Ollama proxy middleware")

    @observe(as_type="generation")
    async def log_event(self) -> None:
        """Log event to langfuse."""

        await self.ollama.is_done

        langfuse_context.update_current_observation(
            input=self.ollama.input_text,
            name=self.ollama.action,
            metadata=self.ollama.response_metadata,
            output=self.ollama.response_content,
            start_time=self.ollama.start_time,
            end_time=self.ollama.completion_stop,
            completion_start_time=self.ollama.completion_start,
            model=self.ollama.model,
            model_parameters=self.ollama.request["options"],
            tags=[self.ollama.action, "ollama", self.ollama.model],
        )

        if not self.ollama.is_done.result():
            raise RuntimeError("Request cancelled")

        try:
            langfuse_context.update_current_observation(
                usage={
                    "input": self.ollama.response_metadata.get("prompt_eval_count"),
                    "output": self.ollama.response_metadata.get("eval_count"),
                    "unit": "TOKENS",
                },
            )
        except Exception as e:
            LOG.exception(e)
            raise e

    @observe(name="pending-request")
    async def observe(self):
        try:
            session = await self.ollama.get_session()

            langfuse_context.update_current_trace(
                input=self.ollama.input_text,
                name=self.ollama.action,
                user_id=self.ollama.user.username,
                session_id=session.id,
            )

            await self.log_event()

            langfuse_context.update_current_trace(
                output=self.ollama.response_content,
            )
        except RuntimeError as e:
            LOG.info(e)
            raise e
        except Exception as e:
            LOG.exception(e)
            raise e


async def langfuse_middleware(
    request: Request,
    call_next: Callable[[Request], Coroutine[Request, None, Response]],
):
    """Log requests to langfuse."""

    LOG.debug("Processing langfuse middleware")

    middleware = LangfuseMiddleware(ollama=getattr(request.state, "ollama", None))
    if middleware.ollama is not None:
        asyncio.run_coroutine_threadsafe(middleware.observe(), asyncio.get_running_loop())

    result = await call_next(request)

    LOG.debug("Langfuse middleware processed")

    return result
