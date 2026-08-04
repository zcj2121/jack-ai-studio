"""AI Chat 的 HTTP 路由。"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError

from app.providers.openai_compatible import (
    OpenAICompatibleProvider,
    ProviderResponseError,
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
    except ProviderResponseError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI Provider returned an invalid response",
        ) from error
