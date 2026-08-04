"""AI Chat 的 HTTP 与 SSE 路由。"""

import json
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import ValidationError

from app.providers.openai_compatible import (
    OpenAICompatibleProvider,
    ProviderError,
    load_provider_config,
)
from app.schemas.chat import ChatMessage, ChatRequest

router = APIRouter(tags=["chat"])


def get_chat_provider() -> OpenAICompatibleProvider:
    """使用服务端配置创建当前 Chat Provider。"""

    try:
        config = load_provider_config()
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Provider is not configured",
        ) from error

    return OpenAICompatibleProvider(config)


ChatProviderDependency = Annotated[
    OpenAICompatibleProvider,
    Depends(get_chat_provider),
]


@router.post(
    "/chat",
    response_model=ChatMessage,
    responses={
        status.HTTP_502_BAD_GATEWAY: {
            "description": "Provider returned an invalid response",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Provider is not configured",
        },
    },
)
async def create_chat_completion(
    request: ChatRequest,
    provider: ChatProviderDependency,
) -> ChatMessage:
    """校验 Chat Request，调用 Provider，并返回 Assistant Message。"""

    try:
        return await provider.generate(request)
    except ProviderError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI Provider returned an invalid response",
        ) from error


def format_sse_event(event: str, data: dict[str, str]) -> str:
    """把事件名称和 JSON 数据编码为一个 SSE Event。"""

    payload = json.dumps(data, ensure_ascii=False)

    return f"event: {event}\ndata: {payload}\n\n"


async def stream_chat_events(
    request: ChatRequest,
    provider: OpenAICompatibleProvider,
) -> AsyncIterator[str]:
    """把 Provider 文本分片转换为项目 SSE 事件。"""

    try:
        async for content in provider.stream(request):
            yield format_sse_event("delta", {"content": content})
    except ProviderError:
        yield format_sse_event(
            "error",
            {"message": "AI Provider streaming failed"},
        )
        return

    yield format_sse_event("done", {})


@router.post(
    "/chat/stream",
    response_class=StreamingResponse,
    responses={
        status.HTTP_200_OK: {
            "content": {
                "text/event-stream": {
                    "schema": {"type": "string"},
                }
            },
            "description": "SSE stream with delta, done, or error events",
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Provider is not configured",
        },
    },
)
async def create_streaming_chat_completion(
    request: ChatRequest,
    provider: ChatProviderDependency,
) -> StreamingResponse:
    """返回逐段传输 Assistant 文本的 SSE Response。"""

    return StreamingResponse(
        stream_chat_events(request, provider),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
