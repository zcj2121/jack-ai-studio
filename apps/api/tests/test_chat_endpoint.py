"""AI Chat Endpoint 的 HTTP 契约测试。"""

import os
from collections.abc import AsyncIterator, Sequence
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.providers.openai_compatible import (
    ProviderCompletion,
    ProviderError,
    ProviderResponseError,
)
from app.routes.chat import get_chat_provider
from app.schemas.chat import ChatRequest
from app.tools.catalog import ChatToolName, ValidatedToolCall
from app.tools.executor import ToolResult


class FakeChatProvider:
    """返回可控结果的 Chat Provider，不读取 Key 或访问网络。"""

    def __init__(self) -> None:
        self.request: ChatRequest | None = None
        self.error: ProviderResponseError | None = None
        self.completion = ProviderCompletion(
            content="这是 Fake Provider 返回的测试回答。"
        )
        self.follow_up_completion = ProviderCompletion(
            content="工具计算结果是 42。"
        )
        self.follow_up: tuple[
            Sequence[ValidatedToolCall],
            Sequence[ToolResult],
        ] | None = None
        self.stream_chunks = ["第一段", "第二段"]
        self.stream_error: ProviderError | None = None

    async def generate_completion(
        self,
        request: ChatRequest,
    ) -> ProviderCompletion:
        self.request = request

        if self.error is not None:
            raise self.error

        return self.completion

    async def generate_tool_follow_up_completion(
        self,
        request: ChatRequest,
        tool_calls: Sequence[ValidatedToolCall],
        tool_results: Sequence[ToolResult],
    ) -> ProviderCompletion:
        self.request = request
        self.follow_up = (tool_calls, tool_results)

        return self.follow_up_completion

    async def stream(
        self,
        request: ChatRequest,
    ) -> AsyncIterator[str]:
        self.request = request

        if self.stream_error is not None:
            raise self.stream_error

        for chunk in self.stream_chunks:
            yield chunk


class ChatEndpointTest(TestCase):
    """验证 POST /chat 的成功、校验和 Provider 错误路径。"""

    def setUp(self) -> None:
        self.provider = FakeChatProvider()
        app.dependency_overrides[get_chat_provider] = lambda: self.provider
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        self.client.close()

    def test_returns_assistant_message(self) -> None:
        response = self.client.post(
            "/chat",
            json={
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "什么是 Dependency Injection？",
                    }
                ],
                "temperature": 0.3,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "role": "assistant",
                "content": "这是 Fake Provider 返回的测试回答。",
            },
        )
        self.assertIsNotNone(self.provider.request)
        self.assertEqual(
            self.provider.request.provider,
            "openai-compatible",
        )
        self.assertEqual(self.provider.request.model, "demo-model")
        self.assertEqual(self.provider.request.temperature, 0.3)
        self.assertIsNone(self.provider.follow_up)

    def test_executes_tool_call_and_returns_final_assistant_message(
        self,
    ) -> None:
        self.provider.completion = ProviderCompletion(
            content=None,
            tool_calls=(
                ValidatedToolCall(
                    id="call_123",
                    name=ChatToolName.ADD_NUMBERS,
                    arguments={"a": 12, "b": 30},
                ),
            ),
        )

        response = self.client.post(
            "/chat",
            json={
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "请计算 12 加 30",
                    }
                ],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "role": "assistant",
                "content": "工具计算结果是 42。",
            },
        )
        self.assertIsNotNone(self.provider.follow_up)
        tool_calls, tool_results = self.provider.follow_up
        self.assertEqual(tool_calls[0].id, "call_123")
        self.assertEqual(tool_results[0].tool_call_id, "call_123")
        self.assertEqual(tool_results[0].content, "42")

    def test_rejects_invalid_request_before_calling_provider(self) -> None:
        response = self.client.post(
            "/chat",
            json={
                "model": "demo-model",
                "messages": [],
            },
        )

        self.assertEqual(response.status_code, 422)
        self.assertIsNone(self.provider.request)

    def test_maps_invalid_provider_response_to_bad_gateway(self) -> None:
        self.provider.error = ProviderResponseError("empty response")

        response = self.client.post(
            "/chat",
            json={
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "你好",
                    }
                ],
            },
        )

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.json(),
            {"detail": "AI Provider returned an invalid response"},
        )

    def test_documents_chat_response_contract(self) -> None:
        paths = self.client.get("/openapi.json").json()["paths"]
        operation = paths["/chat"]["post"]

        self.assertEqual(
            operation["requestBody"]["content"]["application/json"][
                "schema"
            ]["$ref"],
            "#/components/schemas/ChatRequest",
        )
        self.assertEqual(
            operation["responses"]["200"]["content"][
                "application/json"
            ]["schema"]["$ref"],
            "#/components/schemas/ChatMessage",
        )
        self.assertIn("422", operation["responses"])
        self.assertIn("502", operation["responses"])
        self.assertIn("503", operation["responses"])
        self.assertIn("/providers", paths)
        self.assertIn("/chat/stream", paths)
        self.assertIn(
            "text/event-stream",
            paths["/chat/stream"]["post"]["responses"]["200"][
                "content"
            ],
        )

    def test_streams_delta_and_done_events(self) -> None:
        response = self.client.post(
            "/chat/stream",
            json={
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "请流式回答",
                    }
                ],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.headers["content-type"].startswith(
                "text/event-stream"
            )
        )
        self.assertEqual(
            response.text,
            (
                'event: delta\ndata: {"content": "第一段"}\n\n'
                'event: delta\ndata: {"content": "第二段"}\n\n'
                "event: done\ndata: {}\n\n"
            ),
        )

    def test_streams_safe_error_event_after_response_starts(self) -> None:
        self.provider.stream_error = ProviderResponseError(
            "empty stream"
        )

        response = self.client.post(
            "/chat/stream",
            json={
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "你好",
                    }
                ],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.text,
            (
                "event: error\n"
                'data: {"message": "AI Provider streaming failed"}'
                "\n\n"
            ),
        )


class ChatEndpointConfigurationTest(TestCase):
    """验证缺少服务端配置时返回稳定且安全的错误。"""

    def setUp(self) -> None:
        app.dependency_overrides.clear()
        self.client = TestClient(app)

    def tearDown(self) -> None:
        app.dependency_overrides.clear()
        self.client.close()

    def test_returns_service_unavailable_without_api_key(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post(
                "/chat",
                json={
                    "model": "demo-model",
                    "messages": [
                        {
                            "role": "user",
                            "content": "你好",
                        }
                    ],
                },
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {"detail": "AI Provider is not configured"},
        )

    def test_returns_safe_provider_catalog(self) -> None:
        with patch.dict(
            os.environ,
            {
                "AI_PROVIDER_API_KEY": "test-secret",
                "AI_PROVIDER_OPENROUTER_API_KEY": "",
            },
            clear=True,
        ):
            response = self.client.get("/providers")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": "openai-compatible",
                    "label": "OpenAI-compatible",
                    "configured": True,
                },
                {
                    "id": "openrouter",
                    "label": "OpenRouter",
                    "configured": False,
                },
            ],
        )
        self.assertNotIn("test-secret", response.text)

    def test_selects_openrouter_configuration(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post(
                "/chat",
                json={
                    "provider": "openrouter",
                    "model": "demo-model",
                    "messages": [
                        {
                            "role": "user",
                            "content": "你好",
                        }
                    ],
                },
            )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json(),
            {"detail": "AI Provider is not configured"},
        )
