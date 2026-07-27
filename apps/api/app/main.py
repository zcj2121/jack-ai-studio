"""Jack AI Studio API 的最小 Python 程序入口。"""

import sys

SERVICE_INFO: dict[str, str] = {
    "name": "Jack AI Studio API",
    "status": "foundation ready",
}

PLANNED_CAPABILITIES: list[str] = [
    "Provider integration",
    "Conversation management",
    "RAG and Agent services",
]


def format_service_status(
    service_info: dict[str, str],
    capabilities: list[str],
) -> str:
    """把服务信息整理成便于在终端阅读的状态文本。"""

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    capability_summary = ", ".join(capabilities)

    return (
        f"{service_info['name']} | "
        f"status: {service_info['status']} | "
        f"Python: {python_version} | "
        f"planned: {capability_summary}"
    )


def main() -> None:
    """运行 Day 6 的最小状态程序。"""

    print(format_service_status(SERVICE_INFO, PLANNED_CAPABILITIES))
    name: str = "haha"
    print(f"test:{name}")
    dict1: dict[str, int] = {
        "age": 1
    }
    list1: list[str] = ["a", "b"]


if __name__ == "__main__":
    main()
