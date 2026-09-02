"""已校验 Chat Tool Call 的显式执行边界。"""

from collections.abc import Sequence

from pydantic import BaseModel, Field

from app.tools.catalog import (
    AddNumbersArguments,
    ChatToolName,
    ValidatedToolCall,
)


class ToolExecutionError(RuntimeError):
    """工具无法执行或没有对应 Handler。"""


class ToolResult(BaseModel):
    """一次工具执行后准备交给上层的内部结果。"""

    tool_call_id: str = Field(min_length=1)
    name: ChatToolName
    content: str = Field(min_length=1)


def _execute_add_numbers(arguments: AddNumbersArguments) -> str:
    """执行 add_numbers 的纯函数 Handler。"""

    return str(arguments.a + arguments.b)


def execute_tool_call(tool_call: ValidatedToolCall) -> ToolResult:
    """按服务端 allowlist 显式分发一个已校验 Tool Call。"""

    if tool_call.name is ChatToolName.ADD_NUMBERS:
        content = _execute_add_numbers(tool_call.arguments)
    else:
        raise ToolExecutionError(
            f"No Handler registered for tool: {tool_call.name}"
        )

    return ToolResult(
        tool_call_id=tool_call.id,
        name=tool_call.name,
        content=content,
    )


def execute_tool_calls(
    tool_calls: Sequence[ValidatedToolCall],
) -> list[ToolResult]:
    """按 Provider 返回顺序执行多个已校验 Tool Call。"""

    return [execute_tool_call(tool_call) for tool_call in tool_calls]
