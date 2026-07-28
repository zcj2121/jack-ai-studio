"""Jack AI Studio API 的最小 Python 程序入口。"""

import sys

from fastapi import FastAPI
from pydantic import BaseModel, Field, ValidationError

SERVICE_INFO: dict[str, object] = {
    "name": "Jack AI Studio API",
    "status": "foundation ready",
}

PLANNED_CAPABILITIES: list[str] = [
    "Provider integration",
    "Conversation management",
    "RAG and Agent services",
]


class ServiceStatus(BaseModel):
    """经过运行时校验的服务状态数据。"""

    name: str = Field(min_length=1)
    status: str = Field(min_length=1)
    python_version: str = Field(min_length=1)
    planned_capabilities: list[str] = Field(min_length=1)


app = FastAPI(
    title="Jack AI Studio API",
    version="0.1.0",
)


def build_service_status(
    service_info: dict[str, object],
    capabilities: list[str],
) -> ServiceStatus:
    """把普通 Python 数据校验为可信的服务状态模型。"""

    return ServiceStatus.model_validate(
        {
            **service_info,
            "python_version": (
                f"{sys.version_info.major}.{sys.version_info.minor}"
            ),
            "planned_capabilities": capabilities,
        }
    )


def format_service_status(
    service_status: ServiceStatus,
) -> str:
    """把已校验的服务状态整理成便于在终端阅读的文本。"""

    capability_summary = ", ".join(service_status.planned_capabilities)

    return (
        f"{service_status.name} | "
        f"status: {service_status.status} | "
        f"Python: {service_status.python_version} | "
        f"planned: {capability_summary}"
    )


def demonstrate_validation_error() -> str:
    """使用错误数据演示 Pydantic 的运行时校验。"""

    try:
        build_service_status(
            {"name": "", "status": "foundation ready"},
            [],
        )
    except ValidationError as error:
        invalid_fields = ", ".join(
            ".".join(str(part) for part in issue["loc"])
            for issue in error.errors()
        )
        return f"invalid data rejected: {invalid_fields}"

    return "invalid data was not rejected"


@app.get("/health", response_model=ServiceStatus)
async def get_health() -> ServiceStatus:
    """返回经过 Schema 校验的 API 服务状态。"""

    return build_service_status(
        SERVICE_INFO,
        PLANNED_CAPABILITIES,
    )


def main() -> None:
    """运行 Day 7 的 Pydantic 数据校验示例。"""

    service_status = build_service_status(
        SERVICE_INFO,
        PLANNED_CAPABILITIES,
    )
    print(format_service_status(service_status))
    print(demonstrate_validation_error())


if __name__ == "__main__":
    main()
