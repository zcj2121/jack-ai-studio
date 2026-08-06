"""OpenAI-compatible Provider 的最小异步适配器。"""

import os
from collections.abc import AsyncIterator, Mapping

from openai import APIError, AsyncOpenAI
from pydantic import BaseModel, Field, SecretStr, ValidationError

from app.schemas.chat import (
    ChatMessage,
    ChatOutputMode,
    ChatRequest,
    MessageRole,
    StructuredAnswer,
)

API_KEY_ENV_NAME = "AI_PROVIDER_API_KEY"
BASE_URL_ENV_NAME = "AI_PROVIDER_BASE_URL"


class ProviderConfig(BaseModel):
    """只存在于后端的 Provider 连接配置。"""

    api_key: SecretStr = Field(min_length=1)
    base_url: str | None = Field(default=None, min_length=1)


class ProviderError(RuntimeError):
    """Provider 调用的统一业务异常。"""


class ProviderRequestError(ProviderError):
    """Provider 网络或 API 请求失败。"""


class ProviderResponseError(ProviderError):
    """Provider 没有返回可展示的文本。"""


def build_response_format(
    output_mode: ChatOutputMode,
) -> dict[str, object] | None:
    """把项目输出模式转换为 OpenAI-compatible response_format。"""

    if output_mode is ChatOutputMode.TEXT:
        return None

    return {
        "type": "json_schema",
        "json_schema": {
            "name": "jack_ai_structured_answer",
            "strict": True,
            "schema": StructuredAnswer.model_json_schema(),
        },
    }


def validate_structured_answer(content: str) -> str:
    """校验 JSON 内容并返回规范化后的结构化回答。"""

    try:
        answer = StructuredAnswer.model_validate_json(content)
    except ValidationError as error:
        raise ProviderResponseError(
            "Provider response does not match StructuredAnswer schema"
        ) from error

    return answer.model_dump_json()


def load_provider_config(
    environ: Mapping[str, str] | None = None,
    *,
    api_key_env_name: str = API_KEY_ENV_NAME,
    base_url_env_name: str = BASE_URL_ENV_NAME,
    default_base_url: str | None = None,
) -> ProviderConfig:
    """从服务端环境变量读取并校验 Provider 配置。"""

    source = os.environ if environ is None else environ

    return ProviderConfig.model_validate(
        {
            "api_key": source.get(api_key_env_name, "").strip(),
            "base_url": (
                source.get(base_url_env_name, "").strip()
                or default_base_url
            ),
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

    @staticmethod
    def _build_completion_request(
        request: ChatRequest,
        *,
        stream: bool = False,
    ) -> dict[str, object]:
        """构建 Provider 请求参数，并按需附加结构化输出约束。"""

        payload: dict[str, object] = {
            "model": request.model,
            "messages": [
                {
                    "role": message.role.value,
                    "content": message.content,
                }
                for message in request.messages
            ],
            "temperature": request.temperature,
        }

        response_format = build_response_format(request.output_mode)
        if response_format is not None:
            payload["response_format"] = response_format

        if stream:
            payload["stream"] = True

        return payload

    async def generate(self, request: ChatRequest) -> ChatMessage:
        """异步调用 Provider，并返回统一的 Assistant Message。"""

        try:
            completion = await self._client.chat.completions.create(
                **self._build_completion_request(request),
            )
        except APIError as error:
            raise ProviderRequestError(
                "Provider request failed"
            ) from error

        content = completion.choices[0].message.content

        if content is None or not content.strip():
            raise ProviderResponseError(
                "Provider response does not contain assistant text"
            )

        if request.output_mode is ChatOutputMode.STRUCTURED_ANSWER:
            content = validate_structured_answer(content)

        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content=content,
        )

    async def stream(self, request: ChatRequest) -> AsyncIterator[str]:
        """异步读取 Provider Stream，并逐段返回有效文本。"""

        received_content = False
        received_chunks: list[str] = []

        try:
            stream = await self._client.chat.completions.create(
                **self._build_completion_request(request, stream=True),
            )

            async for chunk in stream:
                if not chunk.choices:
                    continue

                content = chunk.choices[0].delta.content

                if content:
                    received_content = True
                    received_chunks.append(content)
                    yield content
        except APIError as error:
            raise ProviderRequestError(
                "Provider streaming request failed"
            ) from error

        if not received_content:
            raise ProviderResponseError(
                "Provider stream does not contain assistant text"
            )

        if request.output_mode is ChatOutputMode.STRUCTURED_ANSWER:
            validate_structured_answer("".join(received_chunks))
