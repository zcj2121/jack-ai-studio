"""AI Chat 请求 Schema 的运行时校验测试。"""

from unittest import TestCase

from pydantic import ValidationError

from app.schemas.chat import ChatRequest, MessageRole


class ChatRequestTest(TestCase):
    """验证 Chat Request 的正常与错误数据边界。"""

    def test_accepts_valid_message_sequence(self) -> None:
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
                        "content": "什么是 Message Role？",
                    },
                ],
            }
        )

        self.assertEqual(request.temperature, 0.7)
        self.assertEqual(request.messages[0].role, MessageRole.SYSTEM)
        self.assertEqual(request.messages[1].role, MessageRole.USER)

    def test_rejects_empty_message_list(self) -> None:
        with self.assertRaises(ValidationError):
            ChatRequest.model_validate(
                {
                    "model": "demo-model",
                    "messages": [],
                }
            )

    def test_rejects_empty_message_content(self) -> None:
        with self.assertRaises(ValidationError):
            ChatRequest.model_validate(
                {
                    "model": "demo-model",
                    "messages": [
                        {
                            "role": "user",
                            "content": "",
                        }
                    ],
                }
            )

    def test_rejects_unknown_message_role(self) -> None:
        with self.assertRaises(ValidationError):
            ChatRequest.model_validate(
                {
                    "model": "demo-model",
                    "messages": [
                        {
                            "role": "visitor",
                            "content": "你好",
                        }
                    ],
                }
            )

    def test_rejects_temperature_outside_supported_range(self) -> None:
        with self.assertRaises(ValidationError):
            ChatRequest.model_validate(
                {
                    "model": "demo-model",
                    "messages": [
                        {
                            "role": "user",
                            "content": "你好",
                        }
                    ],
                    "temperature": 2.1,
                }
            )
