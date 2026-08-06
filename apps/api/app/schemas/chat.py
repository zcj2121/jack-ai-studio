"""AI Chat 的请求数据结构契约。"""

from enum import StrEnum

from pydantic import BaseModel, Field


class MessageRole(StrEnum):
    """一条 Chat Message 在对话中的角色。"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatProviderId(StrEnum):
    """Jack AI Studio 当前支持的 Chat Provider 标识。"""

    OPENAI_COMPATIBLE = "openai-compatible"
    OPENROUTER = "openrouter"


class ChatMessage(BaseModel):
    """发送给模型的一条结构化消息。"""

    role: MessageRole
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    """一次非流式 AI Chat 请求的最小数据契约。"""

    provider: ChatProviderId = ChatProviderId.OPENAI_COMPATIBLE
    model: str = Field(min_length=1)
    messages: list[ChatMessage] = Field(min_length=1)
    temperature: float = Field(default=0.7, ge=0, le=2)


class ChatProviderSummary(BaseModel):
    """允许 Web 展示的 Provider 安全元数据。"""

    id: ChatProviderId
    label: str
    configured: bool
