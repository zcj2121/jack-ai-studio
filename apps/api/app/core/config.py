"""FastAPI 应用配置的服务端边界。"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """从环境变量读取、经过运行时校验的 API 配置。"""

    model_config = SettingsConfigDict(
        env_prefix="JACK_",
        extra="ignore",
        case_sensitive=False,
        frozen=True,
    )

    app_name: str = Field(default="Jack AI Studio API", min_length=1)
    app_version: str = Field(default="0.1.0", min_length=1)
    environment: Literal["development", "test", "production"] = (
        "development"
    )
    api_host: str = Field(default="127.0.0.1", min_length=1)
    api_port: int = Field(default=8000, ge=1, le=65535)
    database_url: str | None = Field(default=None, min_length=1)
    redis_url: str | None = Field(default=None, min_length=1)

    @field_validator("database_url", "redis_url", mode="before")
    @classmethod
    def normalize_optional_urls(cls, value: object) -> object:
        """把空的可选连接配置视为未配置。"""

        if isinstance(value, str) and not value.strip():
            return None
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """返回进程级共享配置，避免每个请求重复读取环境变量。"""

    return Settings()
