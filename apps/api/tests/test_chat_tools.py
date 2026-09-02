"""Tool Calling 服务端数据契约测试。"""

from unittest import TestCase

from pydantic import ValidationError

from app.tools.catalog import (
    ChatToolName,
    RawToolCall,
    ToolCallValidationError,
    get_chat_tool_definitions,
    validate_tool_call,
)


class ChatToolContractTest(TestCase):
    """验证服务端工具定义、allowlist 与参数校验边界。"""

    def test_builds_strict_server_owned_tool_definition(self) -> None:
        definitions = get_chat_tool_definitions()

        self.assertEqual(len(definitions), 1)
        self.assertEqual(definitions[0]["type"], "function")

        function = definitions[0]["function"]

        self.assertIsInstance(function, dict)
        assert isinstance(function, dict)
        self.assertEqual(function["name"], "add_numbers")
        self.assertTrue(function["strict"])

        parameters = function["parameters"]

        self.assertIsInstance(parameters, dict)
        assert isinstance(parameters, dict)
        self.assertEqual(parameters["required"], ["a", "b"])
        self.assertFalse(parameters["additionalProperties"])

    def test_validates_known_tool_and_json_arguments(self) -> None:
        tool_call = RawToolCall(
            id="call_123",
            name="add_numbers",
            arguments='{"a":12,"b":30}',
        )

        validated_call = validate_tool_call(tool_call)

        self.assertEqual(validated_call.id, "call_123")
        self.assertEqual(validated_call.name, ChatToolName.ADD_NUMBERS)
        self.assertEqual(validated_call.arguments.a, 12)
        self.assertEqual(validated_call.arguments.b, 30)

    def test_rejects_blank_tool_call_id(self) -> None:
        with self.assertRaises(ValidationError):
            RawToolCall(
                id="   ",
                name="add_numbers",
                arguments='{"a":12,"b":30}',
            )

    def test_rejects_extra_raw_tool_call_field(self) -> None:
        with self.assertRaises(ValidationError):
            RawToolCall.model_validate(
                {
                    "id": "call_123",
                    "name": "add_numbers",
                    "arguments": '{"a":12,"b":30}',
                    "status": "approved",
                }
            )

    def test_rejects_unknown_tool_name(self) -> None:
        tool_call = RawToolCall(
            id="call_123",
            name="delete_project",
            arguments="{}",
        )

        with self.assertRaises(ToolCallValidationError):
            validate_tool_call(tool_call)

    def test_rejects_malformed_json_arguments(self) -> None:
        tool_call = RawToolCall(
            id="call_123",
            name="add_numbers",
            arguments='{"a":12',
        )

        with self.assertRaises(ToolCallValidationError):
            validate_tool_call(tool_call)

    def test_rejects_missing_tool_argument(self) -> None:
        tool_call = RawToolCall(
            id="call_123",
            name="add_numbers",
            arguments='{"a":12}',
        )

        with self.assertRaises(ToolCallValidationError):
            validate_tool_call(tool_call)

    def test_rejects_wrong_tool_argument_type(self) -> None:
        tool_call = RawToolCall(
            id="call_123",
            name="add_numbers",
            arguments='{"a":"12","b":30}',
        )

        with self.assertRaises(ToolCallValidationError):
            validate_tool_call(tool_call)

    def test_rejects_extra_tool_argument(self) -> None:
        tool_call = RawToolCall(
            id="call_123",
            name="add_numbers",
            arguments='{"a":12,"b":30,"operation":"multiply"}',
        )

        with self.assertRaises(ToolCallValidationError):
            validate_tool_call(tool_call)
