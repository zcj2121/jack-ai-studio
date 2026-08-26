"""OpenAI-compatible Provider 适配器测试。"""

import json
from types import SimpleNamespace
from typing import cast
from unittest import IsolatedAsyncioTestCase, TestCase

from openai import AsyncOpenAI
from pydantic import ValidationError

from app.providers.openai_compatible import (
    build_response_format,
    build_tool_follow_up_messages,
    OpenAICompatibleProvider,
    ProviderConfig,
    ProviderResponseError,
    ProviderToolCallRequested,
    ProviderToolRoundLimitError,
    ToolResultCorrelationError,
    load_provider_config,
)
from app.schemas.chat import ChatOutputMode, ChatRequest, MessageRole
from app.tools.catalog import (
    ChatToolName,
    ValidatedToolCall,
    get_chat_tool_definitions,
)
from app.tools.executor import ToolResult


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


class ProviderToolMessageTest(TestCase):
    """验证 Tool Result 回传消息与调用关联边界。"""

    def setUp(self) -> None:
        self.request = ChatRequest.model_validate(
            {
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "请分别计算 1+2 和 10+20",
                    }
                ],
            }
        )
        self.tool_calls = [
            ValidatedToolCall(
                id="call_first",
                name=ChatToolName.ADD_NUMBERS,
                arguments={"a": 1, "b": 2},
            ),
            ValidatedToolCall(
                id="call_second",
                name=ChatToolName.ADD_NUMBERS,
                arguments={"a": 10, "b": 20},
            ),
        ]
        self.tool_results = [
            ToolResult(
                tool_call_id="call_first",
                name=ChatToolName.ADD_NUMBERS,
                content="3",
            ),
            ToolResult(
                tool_call_id="call_second",
                name=ChatToolName.ADD_NUMBERS,
                content="30",
            ),
        ]

    def test_builds_correlated_tool_follow_up_messages(self) -> None:
        messages = build_tool_follow_up_messages(
            self.request,
            self.tool_calls,
            self.tool_results,
        )

        self.assertEqual(
            messages,
            [
                {
                    "role": "user",
                    "content": "请分别计算 1+2 和 10+20",
                },
                {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_first",
                            "type": "function",
                            "function": {
                                "name": "add_numbers",
                                "arguments": '{"a":1,"b":2}',
                            },
                        },
                        {
                            "id": "call_second",
                            "type": "function",
                            "function": {
                                "name": "add_numbers",
                                "arguments": '{"a":10,"b":20}',
                            },
                        },
                    ],
                },
                {
                    "role": "tool",
                    "tool_call_id": "call_first",
                    "content": "3",
                },
                {
                    "role": "tool",
                    "tool_call_id": "call_second",
                    "content": "30",
                },
            ],
        )

    def test_rejects_follow_up_without_tool_calls(self) -> None:
        with self.assertRaises(ToolResultCorrelationError):
            build_tool_follow_up_messages(self.request, [], [])

    def test_rejects_different_call_and_result_counts(self) -> None:
        with self.assertRaises(ToolResultCorrelationError):
            build_tool_follow_up_messages(
                self.request,
                self.tool_calls,
                self.tool_results[:1],
            )

    def test_rejects_mismatched_result_id_or_name(self) -> None:
        invalid_results = (
            ToolResult(
                tool_call_id="call_unknown",
                name=ChatToolName.ADD_NUMBERS,
                content="3",
            ),
            ToolResult.model_construct(
                tool_call_id="call_first",
                name="future_tool",
                content="3",
            ),
        )

        for invalid_result in invalid_results:
            with self.subTest(invalid_result=invalid_result):
                with self.assertRaises(ToolResultCorrelationError):
                    build_tool_follow_up_messages(
                        self.request,
                        self.tool_calls,
                        [invalid_result, self.tool_results[1]],
                    )

    def test_rejects_duplicate_tool_call_ids(self) -> None:
        duplicate_call = self.tool_calls[1].model_copy(
            update={"id": "call_first"}
        )
        duplicate_result = self.tool_results[1].model_copy(
            update={"tool_call_id": "call_first"}
        )

        with self.assertRaises(ToolResultCorrelationError):
            build_tool_follow_up_messages(
                self.request,
                [self.tool_calls[0], duplicate_call],
                [self.tool_results[0], duplicate_result],
            )


class FakeCompletions:
    """记录调用参数并返回可控响应，不发起真实网络请求。"""

    def __init__(
        self,
        content: str | None,
        stream_contents: list[str | None] | None = None,
        tool_calls: list[object] | None = None,
    ) -> None:
        self.content = content
        self.stream_contents = stream_contents
        self.tool_calls = tool_calls
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
                    message=SimpleNamespace(
                        content=self.content,
                        tool_calls=self.tool_calls,
                    ),
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
        tool_calls: list[object] | None = None,
    ) -> None:
        self.completions = FakeCompletions(
            content,
            stream_contents,
            tool_calls,
        )
        self.chat = SimpleNamespace(completions=self.completions)


class OpenAICompatibleProviderTest(IsolatedAsyncioTestCase):
    """验证异步调用、参数转换与响应边界。"""

    @staticmethod
    def build_tool_follow_up_context(
        *,
        output_mode: ChatOutputMode = ChatOutputMode.TEXT,
    ) -> tuple[ChatRequest, list[ValidatedToolCall], list[ToolResult]]:
        request = ChatRequest(
            model="demo-model",
            messages=[
                {
                    "role": "user",
                    "content": "请计算 12 加 30",
                }
            ],
            temperature=0.2,
            output_mode=output_mode,
        )
        tool_calls = [
            ValidatedToolCall(
                id="call_123",
                name=ChatToolName.ADD_NUMBERS,
                arguments={"a": 12, "b": 30},
            )
        ]
        tool_results = [
            ToolResult(
                tool_call_id="call_123",
                name=ChatToolName.ADD_NUMBERS,
                content="42",
            )
        ]
        return request, tool_calls, tool_results

    async def test_generates_final_completion_after_tool_follow_up(
        self,
    ) -> None:
        client = FakeOpenAIClient("12 加 30 的结果是 42。")
        provider = OpenAICompatibleProvider(
            ProviderConfig(api_key="test-secret"),
            client=cast(AsyncOpenAI, client),
        )
        request, tool_calls, tool_results = (
            self.build_tool_follow_up_context()
        )

        completion = await provider.generate_tool_follow_up_completion(
            request,
            tool_calls,
            tool_results,
        )

        self.assertEqual(completion.content, "12 加 30 的结果是 42。")
        self.assertEqual(completion.tool_calls, ())
        self.assertEqual(
            client.completions.request,
            {
                "model": "demo-model",
                "messages": [
                    {
                        "role": "user",
                        "content": "请计算 12 加 30",
                    },
                    {
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [
                            {
                                "id": "call_123",
                                "type": "function",
                                "function": {
                                    "name": "add_numbers",
                                    "arguments": '{"a":12,"b":30}',
                                },
                            }
                        ],
                    },
                    {
                        "role": "tool",
                        "tool_call_id": "call_123",
                        "content": "42",
                    },
                ],
                "temperature": 0.2,
            },
        )

    async def test_validates_structured_tool_follow_up_completion(
        self,
    ) -> None:
        structured_content = json.dumps(
            {
                "summary": "12 加 30 等于 42。",
                "key_points": ["使用 add_numbers", "结果是 42"],
                "example": "12 + 30 = 42",
                "project_role": "验证工具结果可以形成最终结构化回答。",
            },
            ensure_ascii=False,
        )
        client = FakeOpenAIClient(structured_content)
        provider = OpenAICompatibleProvider(
            ProviderConfig(api_key="test-secret"),
            client=cast(AsyncOpenAI, client),
        )
        request, tool_calls, tool_results = (
            self.build_tool_follow_up_context(
                output_mode=ChatOutputMode.STRUCTURED_ANSWER,
            )
        )

        completion = await provider.generate_tool_follow_up_completion(
            request,
            tool_calls,
            tool_results,
        )

        self.assertEqual(
            json.loads(completion.content or ""),
            json.loads(structured_content),
        )
        self.assertEqual(
            client.completions.request["response_format"],
            build_response_format(ChatOutputMode.STRUCTURED_ANSWER),
        )
        response_format = client.completions.request["response_format"]
        self.assertFalse(
            response_format["json_schema"]["schema"][
                "additionalProperties"
            ]
        )
        self.assertNotIn("tools", client.completions.request)

    async def test_rejects_another_tool_call_after_follow_up(
        self,
    ) -> None:
        client = FakeOpenAIClient(
            None,
            tool_calls=[
                SimpleNamespace(
                    id="call_again",
                    function=SimpleNamespace(
                        name="add_numbers",
                        arguments='{"a":1,"b":2}',
                    ),
                )
            ],
        )
        provider = OpenAICompatibleProvider(
            ProviderConfig(api_key="test-secret"),
            client=cast(AsyncOpenAI, client),
        )
        request, tool_calls, tool_results = (
            self.build_tool_follow_up_context()
        )

        with self.assertRaises(ProviderToolRoundLimitError):
            await provider.generate_tool_follow_up_completion(
                request,
                tool_calls,
                tool_results,
            )

        self.assertNotIn("tools", client.completions.request)

    async def test_rejects_empty_tool_follow_up_text(self) -> None:
        client = FakeOpenAIClient("   ")
        provider = OpenAICompatibleProvider(
            ProviderConfig(api_key="test-secret"),
            client=cast(AsyncOpenAI, client),
        )
        request, tool_calls, tool_results = (
            self.build_tool_follow_up_context()
        )

        with self.assertRaises(ProviderResponseError):
            await provider.generate_tool_follow_up_completion(
                request,
                tool_calls,
                tool_results,
            )

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
                "tools": get_chat_tool_definitions(),
            },
        )

    async def test_parses_validated_tool_call_without_executing_it(self) -> None:
        client = FakeOpenAIClient(
            None,
            tool_calls=[
                SimpleNamespace(
                    id="call_123",
                    function=SimpleNamespace(
                        name="add_numbers",
                        arguments='{"a":12,"b":30}',
                    ),
                )
            ],
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
                        "content": "请计算 12 加 30",
                    }
                ],
            }
        )

        completion = await provider.generate_completion(request)

        self.assertIsNone(completion.content)
        self.assertEqual(len(completion.tool_calls), 1)
        self.assertEqual(completion.tool_calls[0].id, "call_123")
        self.assertEqual(completion.tool_calls[0].name, "add_numbers")
        self.assertEqual(completion.tool_calls[0].arguments.a, 12)
        self.assertEqual(completion.tool_calls[0].arguments.b, 30)
        self.assertEqual(
            client.completions.request["tools"],
            get_chat_tool_definitions(),
        )

    async def test_generate_does_not_execute_tool_call(self) -> None:
        client = FakeOpenAIClient(
            None,
            tool_calls=[
                SimpleNamespace(
                    id="call_123",
                    function=SimpleNamespace(
                        name="add_numbers",
                        arguments='{"a":12,"b":30}',
                    ),
                )
            ],
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
                        "content": "请计算 12 加 30",
                    }
                ],
            }
        )

        with self.assertRaises(ProviderToolCallRequested) as context:
            await provider.generate(request)

        self.assertEqual(
            context.exception.tool_calls[0].arguments.a,
            12,
        )

    async def test_rejects_invalid_provider_tool_call(self) -> None:
        client = FakeOpenAIClient(
            None,
            tool_calls=[
                SimpleNamespace(
                    id="call_123",
                    function=SimpleNamespace(
                        name="add_numbers",
                        arguments='{"a":"12","b":30}',
                    ),
                )
            ],
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
                        "content": "请计算",
                    }
                ],
            }
        )

        with self.assertRaises(ProviderResponseError):
            await provider.generate_completion(request)

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

    async def test_validates_structured_response_and_request_schema(self) -> None:
        structured_content = json.dumps(
            {
                "summary": "Provider Registry 是集中选择表。",
                "key_points": ["使用稳定 ID", "只在后端读取配置"],
                "example": "openrouter -> OpenAICompatibleProvider",
                "project_role": "让 Chat 页面不感知密钥细节。",
            },
            ensure_ascii=False,
        )
        client = FakeOpenAIClient(structured_content)
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
                        "content": "解释 Provider Registry",
                    }
                ],
                "output_mode": "structured_answer",
            }
        )

        message = await provider.generate(request)

        self.assertEqual(
            json.loads(message.content),
            json.loads(structured_content),
        )
        self.assertEqual(
            client.completions.request["response_format"],
            build_response_format(ChatOutputMode.STRUCTURED_ANSWER),
        )

    async def test_rejects_invalid_structured_response(self) -> None:
        client = FakeOpenAIClient('{"summary":"缺少其他字段"}')
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
                "output_mode": "structured_answer",
            }
        )

        with self.assertRaises(ProviderResponseError):
            await provider.generate(request)

    async def test_rejects_extra_structured_response_field(self) -> None:
        client = FakeOpenAIClient(
            json.dumps(
                {
                    "summary": "结构正确但包含额外字段。",
                    "key_points": ["拒绝额外字段"],
                    "example": "unexpected 不属于契约。",
                    "project_role": "保持响应和 JSON Schema 一致。",
                    "unexpected": "not allowed",
                },
                ensure_ascii=False,
            )
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
                        "content": "请结构化回答",
                    }
                ],
                "output_mode": "structured_answer",
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

    async def test_validates_structured_stream_after_all_chunks(self) -> None:
        client = FakeOpenAIClient(
            None,
            [
                '{"summary":"结构化回答",',
                '"key_points":["第一点"],',
                '"example":"一个例子",',
                '"project_role":"项目用途"}',
            ],
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
                        "content": "请结构化回答",
                    }
                ],
                "output_mode": "structured_answer",
            }
        )

        chunks = [chunk async for chunk in provider.stream(request)]

        self.assertEqual(
            "".join(chunks),
            '{"summary":"结构化回答","key_points":["第一点"],'
            '"example":"一个例子","project_role":"项目用途"}',
        )

    async def test_rejects_invalid_structured_stream_after_chunks(self) -> None:
        client = FakeOpenAIClient(
            None,
            ['{"summary":"缺少字段"}'],
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
                        "content": "请结构化回答",
                    }
                ],
                "output_mode": "structured_answer",
            }
        )

        with self.assertRaises(ProviderResponseError):
            _ = [chunk async for chunk in provider.stream(request)]
