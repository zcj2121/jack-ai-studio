# Jack AI Studio API

这里将存放 Jack AI Studio 的 Python API 服务。

Day 6 已建立 Python 程序入口。Day 7 引入 Pydantic 运行时数据校验。Day 8 使用 FastAPI 和 Uvicorn 建立首个只读 HTTP Health Endpoint。Day 9 由 Next.js Server Component 读取该 Endpoint，验证前后端连接。

当前 API 只提供 `GET /health`，用于验证服务存活和响应结构。Day 11 已建立 `ChatMessage` 与 `ChatRequest` 数据契约；Day 12 已建立 OpenAI-compatible Provider 的服务端配置、异步调用和响应转换边界。尚未暴露 Chat Endpoint，也未接入数据库、用户或会话业务。

Next.js 默认使用 `http://127.0.0.1:8000`，也可以复制 `apps/web/.env.example` 中的 `API_BASE_URL` 配置其他后端地址。

## 运行终端示例

在仓库根目录执行：

```bash
uv run python apps/api/app/main.py
```

`uv` 会根据根目录的 `pyproject.toml` 和 `uv.lock` 使用已锁定的依赖版本。

## 启动 HTTP API

```bash
pnpm dev:api
```

启动后访问：

- Health Endpoint：`http://127.0.0.1:8000/health`
- OpenAPI 文档：`http://127.0.0.1:8000/docs`

## 自动化测试

在仓库根目录执行：

```bash
pnpm test:api
```

当前测试覆盖 Health 路由函数与注册契约，以及 Chat Message Role、非空消息和 Temperature 范围等运行时数据边界。单元测试不代替真实 HTTP 联调。

Day 12 的 Provider 单元测试使用 Mock Client，不读取真实 Key、不请求外部模型，也不消耗 Provider 额度。可用的服务端环境变量名称记录在 `apps/api/.env.example`。

## 计划职责

- 保护模型 Provider 的 API Key。
- 统一处理模型调用、业务规则和错误。
- 提供用户、会话、RAG、Agent、MCP 与 Workflow API。
- 记录日志、用量和工具调用审计信息。
