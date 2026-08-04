"""OpenAI-compatible Provider 适配器测试。"""

from types import SimpleNamespace
from typing import cast
from unittest import IsolatedAsyncioTestCase, TestCase

from openai import AsyncOpenAI
from pydantic import ValidationError

from app.providers.openai_compatible import (
    OpenAICompatibleProvider,
    ProviderConfig,
    ProviderResponseError,
    load_provider_config,
)
from app.schemas.chat import ChatRequest, MessageRole


class ProviderConfigTest(TestCase):
    """验证 Provider 配置只接受完整的服务端数据。"""

    def test_loads_api_key_and_optional_base_url(self) -> None:
        config = load_provider_config(
            {
                "AI_PROVIDER_API_KEY": "test-secret",
                "AI_PROVIDER_BASE_URL": "https://provider.example/v1",
            }
        )

        self.assertEqual(
            config.api_key.get_secret_value(),
            "test-secret",
        )
        self.assertEqual(
            config.base_url,
            "https://provider.example/v1",
        )
        self.assertNotIn("test-secret", repr(config))

    def test_rejects_missing_api_key(self) -> None:
        with self.assertRaises(ValidationError):
            load_provider_config({})


class FakeCompletions:
    """记录调用参数并返回可控响应，不发起真实网络请求。"""

    def __init__(
        self,
        content: str | None,
        stream_contents: list[str | None] | None = None,
    ) -> None:
        self.content = content
        self.stream_contents = stream_contents
        self.request: dict[str, object] | None = None

    async def create(self, **request: object) -> object:
        self.request = request

        if request.get("stream") is True:
            return FakeChatCompletionStream(
                self.stream_contents or []
            )

        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content=self.content),
                )
            ]
        )


class FakeChatCompletionStream:
    """按顺序生成 Chat Completion Chunk 的异步迭代器。"""

    def __init__(self, contents: list[str | None]) -> None:
        self._contents = iter(contents)

    def __aiter__(self) -> "FakeChatCompletionStream":
        return self

    async def __anext__(self) -> object:
        try:
            content = next(self._contents)
        except StopIteration as error:
            raise StopAsyncIteration from error

        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    delta=SimpleNamespace(content=content),
                )
            ]
        )


class FakeOpenAIClient:
    """提供 Provider 当前需要的最小 SDK 结构。"""

    def __init__(
        self,
        content: str | None,
        stream_contents: list[str | None] | None = None,
    ) -> None:
        self.completions = FakeCompletions(
            content,
            stream_contents,
        )
        self.chat = SimpleNamespace(completions=self.completions)


class OpenAICompatibleProviderTest(IsolatedAsyncioTestCase):
    """验证异步调用、参数转换与响应边界。"""

    async def test_generates_assistant_message(self) -> None:
        client = FakeOpenAIClient("这是 Provider 返回的文本。")
        provider = OpenAICompatibleProvider(
            ProviderConfig(api_key="test-secret"),
            client=cast(AsyncOpenAI, client),
        )
        request = ChatRequest.model_validate(
            {
                "model": "demo-model",
                "messages": [
                    {
                        "role": "system",
                        "content": "请使用中文回答。",
                    },
                    {
                        "role": "user",
                        "content": "什么是 Provider Adapter？",
                    },
                ],
                "temperature": 0.3,
            }
        )

        message = await provider.generate(request)

        self.assertEqual(message.role, MessageRole.ASSISTANT)
        self.assertEqual(message.content, "这是 Provider 返回的文本。")
        self.assertEqual(
            client.completions.request,
            {
                "model": "demo-model",
                "messages": [
                    {
                        "role": "system",
                        "content": "请使用中文回答。",
                    },
                    {
                        "role": "user",
                        "content": "什么是 Provider Adapter？",
                    },
                ],
                "temperature": 0.3,
            },
        )

    async def test_rejects_empty_provider_text(self) -> None:
        client = FakeOpenAIClient("   ")
        provider = OpenAICompatibleProvider(
            ProviderConfig(api_key="test-secret"),
            client=cast(AsyncOpenAI, client),
        )
        request = ChatRequest.model_validate(
            {
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "你好",
                    }
                ],
            }
        )

        with self.assertRaises(ProviderResponseError):
            await provider.generate(request)

    async def test_streams_assistant_text_chunks(self) -> None:
        client = FakeOpenAIClient(
            None,
            ["第一段", None, "", "第二段"],
        )
        provider = OpenAICompatibleProvider(
            ProviderConfig(api_key="test-secret"),
            client=cast(AsyncOpenAI, client),
        )
        request = ChatRequest.model_validate(
            {
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "请流式回答",
                    }
                ],
            }
        )

        chunks = [chunk async for chunk in provider.stream(request)]

        self.assertEqual(chunks, ["第一段", "第二段"])
        self.assertEqual(
            client.completions.request,
            {
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "请流式回答",
                    }
                ],
                "temperature": 0.7,
                "stream": True,
            },
        )

    async def test_rejects_stream_without_text(self) -> None:
        client = FakeOpenAIClient(None, [None, ""])
        provider = OpenAICompatibleProvider(
            ProviderConfig(api_key="test-secret"),
            client=cast(AsyncOpenAI, client),
        )
        request = ChatRequest.model_validate(
            {
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "你好",
                    }
                ],
            }
        )

        with self.assertRaises(ProviderResponseError):
            _ = [chunk async for chunk in provider.stream(request)]
