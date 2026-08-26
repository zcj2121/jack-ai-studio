"""AI Chat 的固定单轮工具编排。"""

from app.providers.openai_compatible import OpenAICompatibleProvider
from app.schemas.chat import ChatMessage, ChatRequest, MessageRole
from app.tools.executor import ToolExecutionError, execute_tool_calls


class ChatOrchestrationError(RuntimeError):
    """Chat 固定流程无法生成最终 Assistant Message。"""


async def orchestrate_chat_completion(
    request: ChatRequest,
    provider: OpenAICompatibleProvider,
) -> ChatMessage:
    """完成文本响应或一次 Tool Call 回传，并生成对外消息。"""

    completion = await provider.generate_completion(request)

    if completion.tool_calls:
        try:
            tool_results = execute_tool_calls(completion.tool_calls)
        except ToolExecutionError as error:
            raise ChatOrchestrationError(
                "Chat tool execution failed"
            ) from error

        completion = await provider.generate_tool_follow_up_completion(
            request,
            completion.tool_calls,
            tool_results,
        )

    if completion.content is None:
        raise ChatOrchestrationError(
            "Chat orchestration did not produce assistant text"
        )

    return ChatMessage(
        role=MessageRole.ASSISTANT,
        content=completion.content,
    )
