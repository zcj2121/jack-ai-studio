"""FastAPI 应用配置的运行时校验测试。"""

import os
from unittest import TestCase
from unittest.mock import patch

from pydantic import ValidationError

from app.core.config import Settings, get_settings


class SettingsTest(TestCase):
    """验证配置默认值、环境变量和非法输入边界。"""

    def tearDown(self) -> None:
        get_settings.cache_clear()

    def test_uses_safe_local_defaults(self) -> None:
        settings = Settings(_env_file=None)

        self.assertEqual(settings.app_name, "Jack AI Studio API")
        self.assertEqual(settings.environment, "development")
        self.assertEqual(settings.api_host, "127.0.0.1")
        self.assertEqual(settings.api_port, 8000)
        self.assertIsNone(settings.database_url)
        self.assertIsNone(settings.redis_url)

    def test_reads_prefixed_environment_variables(self) -> None:
        with patch.dict(
            os.environ,
            {
                "JACK_ENVIRONMENT": "test",
                "JACK_API_PORT": "9000",
                "JACK_DATABASE_URL": "postgresql+asyncpg://localhost/jack",
                "JACK_REDIS_URL": "redis://localhost:6379/0",
            },
            clear=False,
        ):
            settings = get_settings()

        self.assertEqual(settings.environment, "test")
        self.assertEqual(settings.api_port, 9000)
        self.assertEqual(
            settings.database_url,
            "postgresql+asyncpg://localhost/jack",
        )
        self.assertEqual(settings.redis_url, "redis://localhost:6379/0")

    def test_blank_optional_urls_are_treated_as_unconfigured(self) -> None:
        settings = Settings(
            _env_file=None,
            database_url=" ",
            redis_url="",
        )

        self.assertIsNone(settings.database_url)
        self.assertIsNone(settings.redis_url)

    def test_rejects_invalid_environment_and_port(self) -> None:
        with self.assertRaises(ValidationError):
            Settings(_env_file=None, environment="staging")

        with self.assertRaises(ValidationError):
            Settings(_env_file=None, api_port=70000)
