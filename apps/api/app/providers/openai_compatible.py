"""OpenAI-compatible Provider 的最小异步适配器。"""

import os
from collections.abc import AsyncIterator, Mapping, Sequence
from dataclasses import dataclass

from openai import APIError, AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from pydantic import BaseModel, Field, SecretStr, ValidationError

from app.schemas.chat import (
    ChatMessage,
    ChatOutputMode,
    ChatRequest,
    MessageRole,
    StructuredAnswer,
)
from app.tools.catalog import (
    RawToolCall,
    ToolCallValidationError,
    ValidatedToolCall,
    get_chat_tool_definitions,
    validate_tool_call,
)
from app.tools.executor import ToolResult

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


class ProviderToolCallRequested(ProviderError):
    """Provider 返回了已校验、但当前 Chat 尚未执行的工具请求。"""

    def __init__(
        self,
        tool_calls: tuple[ValidatedToolCall, ...],
    ) -> None:
        self.tool_calls = tool_calls
        super().__init__("Provider requested tool calls")


class ToolResultCorrelationError(ValueError):
    """Tool Result 无法和原始 Tool Call 一一对应。"""


@dataclass(frozen=True)
class ProviderCompletion:
    """Provider 一次非流式响应的内部结果。"""

    content: str | None
    tool_calls: tuple[ValidatedToolCall, ...] = ()


def build_tool_follow_up_messages(
    request: ChatRequest,
    tool_calls: Sequence[ValidatedToolCall],
    tool_results: Sequence[ToolResult],
) -> list[dict[str, object]]:
    """构造回传 Tool Result 所需的 OpenAI-compatible 消息序列。"""

    if not tool_calls:
        raise ToolResultCorrelationError(
            "Tool follow-up requires at least one tool call"
        )

    if len(tool_calls) != len(tool_results):
        raise ToolResultCorrelationError(
            "Tool calls and results must have the same length"
        )

    tool_call_ids = [tool_call.id for tool_call in tool_calls]
    if len(set(tool_call_ids)) != len(tool_call_ids):
        raise ToolResultCorrelationError(
            "Tool call IDs must be unique"
        )

    assistant_tool_calls: list[dict[str, object]] = []
    tool_messages: list[dict[str, object]] = []

    for tool_call, tool_result in zip(tool_calls, tool_results):
        if (
            tool_result.tool_call_id != tool_call.id
            or tool_result.name is not tool_call.name
        ):
            raise ToolResultCorrelationError(
                "Tool result does not match the original tool call"
            )

        assistant_tool_calls.append(
            {
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.name.value,
                    "arguments": tool_call.arguments.model_dump_json(),
                },
            }
        )
        tool_messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_result.tool_call_id,
                "content": tool_result.content,
            }
        )

    return [
        *[
            {
                "role": message.role.value,
                "content": message.content,
            }
            for message in request.messages
        ],
        {
            "role": "assistant",
            "content": None,
            "tool_calls": assistant_tool_calls,
        },
        *tool_messages,
    ]


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
        include_tools: bool = False,
    ) -> dict[str, object]:
        """构建 Provider 请求参数，并按需附加输出和工具约束。"""

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

        if include_tools:
            payload["tools"] = get_chat_tool_definitions()

        if stream:
            payload["stream"] = True

        return payload

    @staticmethod
    def _parse_tool_calls(
        message: ChatCompletionMessage,
    ) -> tuple[ValidatedToolCall, ...]:
        """把 Provider Tool Call 转换为通过服务端契约的调用对象。"""

        raw_tool_calls = getattr(message, "tool_calls", None) or []
        validated_tool_calls: list[ValidatedToolCall] = []

        for raw_tool_call in raw_tool_calls:
            function = getattr(raw_tool_call, "function", None)
            raw_call = {
                "id": getattr(raw_tool_call, "id", ""),
                "name": getattr(function, "name", ""),
                "arguments": getattr(function, "arguments", ""),
            }

            try:
                validated_raw_call = RawToolCall.model_validate(raw_call)
                validated_tool_calls.append(
                    validate_tool_call(validated_raw_call)
                )
            except (ToolCallValidationError, ValidationError) as error:
                raise ProviderResponseError(
                    "Provider returned an invalid tool call"
                ) from error

        return tuple(validated_tool_calls)

    @classmethod
    def _parse_completion(
        cls,
        completion: ChatCompletion,
        request: ChatRequest,
    ) -> ProviderCompletion:
        """解析文本或 Tool Call，避免把未校验数据交给执行层。"""

        try:
            message = completion.choices[0].message
        except (AttributeError, IndexError, TypeError) as error:
            raise ProviderResponseError(
                "Provider response does not contain an assistant message"
            ) from error

        tool_calls = cls._parse_tool_calls(message)
        content = getattr(message, "content", None)

        if tool_calls:
            return ProviderCompletion(
                content=content,
                tool_calls=tool_calls,
            )

        if content is None or not content.strip():
            raise ProviderResponseError(
                "Provider response does not contain assistant text"
            )

        if request.output_mode is ChatOutputMode.STRUCTURED_ANSWER:
            content = validate_structured_answer(content)

        return ProviderCompletion(content=content)

    async def generate_completion(
        self,
        request: ChatRequest,
    ) -> ProviderCompletion:
        """发送服务端 Tool Definition，并解析 Provider 非流式响应。"""

        try:
            completion = await self._client.chat.completions.create(
                **self._build_completion_request(
                    request,
                    include_tools=True,
                ),
            )
        except APIError as error:
            raise ProviderRequestError(
                "Provider request failed"
            ) from error

        return self._parse_completion(completion, request)

    async def generate(self, request: ChatRequest) -> ChatMessage:
        """异步调用 Provider，并返回统一的 Assistant Message。"""

        completion = await self.generate_completion(request)

        if completion.tool_calls:
            raise ProviderToolCallRequested(completion.tool_calls)

        if completion.content is None:
            raise ProviderResponseError(
                "Provider response does not contain assistant text"
            )

        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content=completion.content,
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
