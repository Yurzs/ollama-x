from typing import Any

from pydantic import BaseModel, Field

PASSTHROUGH = {
    "default_system_message": "You are a coding assistant that outputs short answers, gives links to documentation."
}
FIM_PSM = {}


class ModelRecord(BaseModel):
    n_ctx: int = 1048
    supports_scratchpads: dict[str, Any] = Field(default={"PASSTHROUGH": PASSTHROUGH})
    default_scratchpad: None | str = "PASSTHROUGH"
    similar_models: list[str] = Field(default_factory=list)
    supports_tools: bool = False

    @classmethod
    def from_model(cls, model: "OllamaModel"):
        arch = model.info["general.architecture"]

        return cls(
            n_ctx=model.info[f"{arch}.context_length"],
            supports_scratchpads={
                "PASSTHROUGH": PASSTHROUGH,
            },
        )


class RefactCapsBase(BaseModel):
    cloud_name: str
    endpoint_template: str
    endpoint_style: str = Field("openai")
    tokenizer_path_template: None | str = None
    tokenizer_rewrite_path: dict[str, str] = Field(default_factory=dict)
    code_completion_default_model: str
    code_completion_n_ctx: int
    code_chat_default_model: str
    telemetry_basic_dest: str
    telemetry_corrected_snippets_dest: None | str = None
    running_models: list[str] = Field(default_factory=list)


class RefactCodeAssistantCaps(RefactCapsBase):
    endpoint_chat_passthrough: None | str = None
    telemetry_basic_retrieve_my_own: None | str = None
    code_completion_models: None | dict[str, ModelRecord] = Field(None)
    code_chat_models: None | dict[str, ModelRecord] = Field(None)
    models_dict_patch: None | dict[str, ModelRecord] = Field(None)
    default_embeddings_model: None | str = None
    endpoint_embeddings_template: None | str = None
    endpoint_embeddings_style: None | str = None
    size_embeddings: None | int = None
    embedding_n_ctx: None | int = None
    caps_version: None | int = 1
    code_chat_default_system_prompt: None | str = None
    customization: None | str = None
