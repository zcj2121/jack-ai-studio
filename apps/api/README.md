# Jack AI Studio API

这里将存放 Jack AI Studio 的 Python API 服务。

Day 6 已建立 Python 程序入口。Day 7 引入 Pydantic 运行时数据校验。Day 8 使用 FastAPI 和 Uvicorn 建立首个只读 HTTP Health Endpoint。Day 9 由 Next.js Server Component 读取该 Endpoint，验证前后端连接。

当前 API 只提供 `GET /health`，用于验证服务存活和响应结构。尚未接入模型、数据库、用户或会话业务。

Next.js 默认使用 `http://127.0.0.1:8000`，也可以复制 `apps/web/.env.example` 中的 `API_BASE_URL` 配置其他后端地址。

## 运行终端示例

在仓库根目录执行：

```bash
uv run python apps/api/app/main.py
```

`uv` 会根据根目录的 `pyproject.toml` 和 `uv.lock` 使用已锁定的依赖版本。

## 启动 HTTP API

```bash
uv run uvicorn app.main:app --app-dir apps/api --host 127.0.0.1 --port 8000
```

启动后访问：

- Health Endpoint：`http://127.0.0.1:8000/health`
- OpenAPI 文档：`http://127.0.0.1:8000/docs`

## 计划职责

- 保护模型 Provider 的 API Key。
- 统一处理模型调用、业务规则和错误。
- 提供用户、会话、RAG、Agent、MCP 与 Workflow API。
- 记录日志、用量和工具调用审计信息。
