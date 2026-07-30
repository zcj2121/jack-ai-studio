"""OpenAI-compatible Provider 的最小异步适配器。"""

import os
from collections.abc import Mapping

from openai import AsyncOpenAI
from pydantic import BaseModel, Field, SecretStr

from app.schemas.chat import ChatMessage, ChatRequest, MessageRole

API_KEY_ENV_NAME = "AI_PROVIDER_API_KEY"
BASE_URL_ENV_NAME = "AI_PROVIDER_BASE_URL"


class ProviderConfig(BaseModel):
    """只存在于后端的 Provider 连接配置。"""

    api_key: SecretStr = Field(min_length=1)
    base_url: str | None = Field(default=None, min_length=1)


class ProviderResponseError(RuntimeError):
    """Provider 没有返回可展示的文本。"""


def load_provider_config(
    environ: Mapping[str, str] | None = None,
) -> ProviderConfig:
    """从服务端环境变量读取并校验 Provider 配置。"""

    source = os.environ if environ is None else environ

    return ProviderConfig.model_validate(
        {
            "api_key": source.get(API_KEY_ENV_NAME, ""),
            "base_url": source.get(BASE_URL_ENV_NAME) or None,
        }
    )


class OpenAICompatibleProvider:
    """把项目 ChatRequest 转换为 OpenAI-compatible 请求。"""

    def __init__(
        self,
        config: ProviderConfig,
        client: AsyncOpenAI | None = None,
    ) -> None:
        if client is not None:
            self._client = client
        elif config.base_url is None:
            self._client = AsyncOpenAI(
                api_key=config.api_key.get_secret_value(),
            )
        else:
            self._client = AsyncOpenAI(
                api_key=config.api_key.get_secret_value(),
                base_url=config.base_url,
            )

    async def generate(self, request: ChatRequest) -> ChatMessage:
        """异步调用 Provider，并返回统一的 Assistant Message。"""

        completion = await self._client.chat.completions.create(
            model=request.model,
            messages=[
                {
                    "role": message.role.value,
                    "content": message.content,
                }
                for message in request.messages
            ],
            temperature=request.temperature,
        )
        content = completion.choices[0].message.content

        if content is None or not content.strip():
            raise ProviderResponseError(
                "Provider response does not contain assistant text"
            )

        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content=content,
        )
