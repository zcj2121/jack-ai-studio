"""AI Chat Endpoint 的 HTTP 契约测试。"""

import os
from unittest import TestCase
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.providers.openai_compatible import ProviderResponseError
from app.routes.chat import get_chat_provider
from app.schemas.chat import ChatMessage, ChatRequest, MessageRole


class FakeChatProvider:
    """返回可控结果的 Chat Provider，不读取 Key 或访问网络。"""

    def __init__(self) -> None:
        self.request: ChatRequest | None = None
        self.error: ProviderResponseError | None = None

    async def generate(self, request: ChatRequest) -> ChatMessage:
        self.request = request

        if self.error is not None:
            raise self.error

        return ChatMessage(
            role=MessageRole.ASSISTANT,
            content="这是 Fake Provider 返回的测试回答。",
        )


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
        self.assertEqual(self.provider.request.model, "demo-model")
        self.assertEqual(self.provider.request.temperature, 0.3)

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
        operation = self.client.get("/openapi.json").json()["paths"][
            "/chat"
        ]["post"]

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
