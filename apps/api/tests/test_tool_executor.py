"""Tool Executor 执行边界测试。"""

from unittest import TestCase

from app.tools.catalog import ChatToolName, ValidatedToolCall
from app.tools.executor import (
    ToolExecutionError,
    execute_tool_call,
    execute_tool_calls,
)


def build_tool_call(
    call_id: str,
    a: int,
    b: int,
) -> ValidatedToolCall:
    """构造测试使用的已校验 Tool Call。"""

    return ValidatedToolCall(
        id=call_id,
        name=ChatToolName.ADD_NUMBERS,
        arguments={"a": a, "b": b},
    )


class ToolExecutorTest(TestCase):
    """验证显式 Handler、调用 ID 和多调用顺序。"""

    def test_executes_add_numbers_and_preserves_call_id(self) -> None:
        result = execute_tool_call(
            build_tool_call("call_123", 12, 30)
        )

        self.assertEqual(result.tool_call_id, "call_123")
        self.assertEqual(result.name, ChatToolName.ADD_NUMBERS)
        self.assertEqual(result.content, "42")

    def test_executes_multiple_calls_in_provider_order(self) -> None:
        results = execute_tool_calls(
            [
                build_tool_call("call_first", 1, 2),
                build_tool_call("call_second", 10, 20),
            ]
        )

        self.assertEqual(
            [(result.tool_call_id, result.content) for result in results],
            [("call_first", "3"), ("call_second", "30")],
        )

    def test_rejects_a_validated_call_without_a_registered_handler(self) -> None:
        unsupported_call = ValidatedToolCall.model_construct(
            id="call_unsupported",
            name="future_tool",
            arguments={"a": 1, "b": 2},
        )

        with self.assertRaises(ToolExecutionError):
            execute_tool_call(unsupported_call)
