"""Chat Provider 注册表测试。"""

from unittest import TestCase

from pydantic import ValidationError

from app.providers.registry import (
    create_chat_provider,
    get_provider_definition,
    list_chat_providers,
)
from app.schemas.chat import ChatProviderId


class ProviderRegistryTest(TestCase):
    """验证 Provider 目录、环境变量隔离与默认 Base URL。"""

    def test_lists_safe_provider_catalog(self) -> None:
        providers = list_chat_providers(
            {
                "AI_PROVIDER_API_KEY": "openai-secret",
                "AI_PROVIDER_OPENROUTER_API_KEY": "",
            }
        )

        self.assertEqual(
            [provider.model_dump(mode="json") for provider in providers],
            [
                {
                    "id": "openai-compatible",
                    "label": "OpenAI-compatible",
                    "configured": True,
                },
                {
                    "id": "openrouter",
                    "label": "OpenRouter",
                    "configured": False,
                },
            ],
        )
        self.assertNotIn("openai-secret", repr(providers))

    def test_creates_openrouter_provider_with_default_base_url(self) -> None:
        provider = create_chat_provider(
            ChatProviderId.OPENROUTER,
            {
                "AI_PROVIDER_OPENROUTER_API_KEY": "router-secret",
            },
        )

        self.assertEqual(
            str(provider._client.base_url),
            "https://openrouter.ai/api/v1/",
        )
        self.assertNotIn("router-secret", repr(provider))

    def test_rejects_unconfigured_selected_provider(self) -> None:
        with self.assertRaises(ValidationError):
            create_chat_provider(ChatProviderId.OPENROUTER, {})

    def test_returns_definition_for_supported_provider(self) -> None:
        definition = get_provider_definition(
            ChatProviderId.OPENAI_COMPATIBLE
        )

        self.assertEqual(
            definition.api_key_env_name,
            "AI_PROVIDER_API_KEY",
        )
