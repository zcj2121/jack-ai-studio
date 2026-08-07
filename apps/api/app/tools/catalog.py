"""Chat 可用工具的服务端定义与调用参数校验。"""

from enum import StrEnum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
)


class ChatToolName(StrEnum):
    """Jack AI Studio 当前允许模型请求的工具名。"""

    ADD_NUMBERS = "add_numbers"


class AddNumbersArguments(BaseModel):
    """add_numbers 工具允许接收的参数。"""

    model_config = ConfigDict(extra="forbid", strict=True)

    a: int
    b: int


class RawToolCall(BaseModel):
    """Provider 返回、尚未获得应用信任的 Tool Call。"""

    model_config = ConfigDict(extra="forbid", strict=True)

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    arguments: str = Field(min_length=1)

    @field_validator("id", "name", "arguments")
    @classmethod
    def reject_blank_string(cls, value: str) -> str:
        """拒绝只包含空白字符的 Tool Call 字段。"""

        if not value.strip():
            raise ValueError("Tool call fields must not be blank")

        return value


class ValidatedToolCall(BaseModel):
    """工具名和参数都通过服务端校验的 Tool Call。"""

    id: str = Field(min_length=1)
    name: ChatToolName
    arguments: AddNumbersArguments


class ToolCallValidationError(ValueError):
    """Provider Tool Call 不符合项目工具契约。"""


def get_chat_tool_definitions() -> list[dict[str, object]]:
    """构建未来发送给 Provider 的服务端 Tool Definition。"""

    return [
        {
            "type": "function",
            "function": {
                "name": ChatToolName.ADD_NUMBERS.value,
                "description": "Add two integers and return their sum.",
                "parameters": AddNumbersArguments.model_json_schema(),
                "strict": True,
            },
        }
    ]


def validate_tool_call(tool_call: RawToolCall) -> ValidatedToolCall:
    """按 allowlist 和 Pydantic Schema 校验 Provider Tool Call。"""

    try:
        tool_name = ChatToolName(tool_call.name)
    except ValueError as error:
        raise ToolCallValidationError(
            "Provider requested an unsupported tool"
        ) from error

    if tool_name is not ChatToolName.ADD_NUMBERS:
        raise ToolCallValidationError(
            "Provider requested an unsupported tool"
        )

    try:
        arguments = AddNumbersArguments.model_validate_json(
            tool_call.arguments
        )
    except ValidationError as error:
        raise ToolCallValidationError(
            "Provider returned invalid tool arguments"
        ) from error

    return ValidatedToolCall(
        id=tool_call.id,
        name=tool_name,
        arguments=arguments,
    )
