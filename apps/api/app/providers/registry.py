"""Chat Provider 注册表与服务端配置选择。"""

import os
from collections.abc import Mapping
from dataclasses import dataclass

from app.providers.openai_compatible import (
    OpenAICompatibleProvider,
    load_provider_config,
)
from app.schemas.chat import ChatProviderId, ChatProviderSummary


@dataclass(frozen=True)
class ProviderDefinition:
    """一个 Provider 的公开信息与私有环境变量映射。"""

    id: ChatProviderId
    label: str
    api_key_env_name: str
    base_url_env_name: str
    default_base_url: str | None = None


PROVIDER_DEFINITIONS = (
    ProviderDefinition(
        id=ChatProviderId.OPENAI_COMPATIBLE,
        label="OpenAI-compatible",
        api_key_env_name="AI_PROVIDER_API_KEY",
        base_url_env_name="AI_PROVIDER_BASE_URL",
    ),
    ProviderDefinition(
        id=ChatProviderId.OPENROUTER,
        label="OpenRouter",
        api_key_env_name="AI_PROVIDER_OPENROUTER_API_KEY",
        base_url_env_name="AI_PROVIDER_OPENROUTER_BASE_URL",
        default_base_url="https://openrouter.ai/api/v1",
    ),
)


def get_provider_definition(
    provider_id: ChatProviderId,
) -> ProviderDefinition:
    """按稳定 ID 取得 Provider 定义。"""

    for definition in PROVIDER_DEFINITIONS:
        if definition.id == provider_id:
            return definition

    raise ValueError(f"Unsupported Provider: {provider_id}")


def list_chat_providers(
    environ: Mapping[str, str] | None = None,
) -> list[ChatProviderSummary]:
    """列出 Web 可见的 Provider 信息，不暴露密钥或 Base URL。"""

    source = os.environ if environ is None else environ

    return [
        ChatProviderSummary(
            id=definition.id,
            label=definition.label,
            configured=bool(
                source.get(definition.api_key_env_name, "").strip()
            ),
        )
        for definition in PROVIDER_DEFINITIONS
    ]


def create_chat_provider(
    provider_id: ChatProviderId,
    environ: Mapping[str, str] | None = None,
) -> OpenAICompatibleProvider:
    """使用所选 Provider 的服务端配置创建统一 Adapter。"""

    definition = get_provider_definition(provider_id)
    config = load_provider_config(
        environ,
        api_key_env_name=definition.api_key_env_name,
        base_url_env_name=definition.base_url_env_name,
        default_base_url=definition.default_base_url,
    )

    return OpenAICompatibleProvider(config)
