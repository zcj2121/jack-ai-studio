# Jack AI Studio API

这里将存放 Jack AI Studio 的 Python API 服务。

Day 6 已建立 Python 程序入口。Day 7 引入 Pydantic 运行时数据校验。Day 8 使用 FastAPI 和 Uvicorn 建立首个只读 HTTP Health Endpoint。Day 9 由 Next.js Server Component 读取该 Endpoint，验证前后端连接。

当前 API 提供 `GET /health`、`GET /providers`、`POST /chat` 与 `POST /chat/stream`。Day 11～18 建立 Chat 契约、Provider Adapter、HTTP/SSE、多 Provider 与 Structured Output；Day 19～24 完成严格 Tool Call 校验、Executor、Tool Result Follow-up 和固定单轮 Chat Orchestrator；Day 26 新增 `app/core/config.py`，统一校验 `JACK_` 前缀的应用配置；Day 27 新增 `app/db/session.py`，建立 SQLAlchemy AsyncEngine 和请求范围 AsyncSession 边界；Day 28 新增 `app/db/base.py`、`app/models/user.py` 与 `app/repositories/user.py`，建立最小 ORM Model/Repository 边界；Day 29 新增 `alembic.ini`、`app/alembic/env.py` 和 `users` 表初始 revision，建立 Migration 边界。当前未执行真实数据库 Migration、用户 HTTP 或会话业务，也不支持多轮 Agent Loop。

Next.js 默认使用 `http://127.0.0.1:8000`，也可以复制 `apps/web/.env.example` 中的 `API_BASE_URL` 配置其他后端地址。

## 运行终端示例

在仓库根目录执行：

```bash
uv run python apps/api/app/main.py
```

`uv` 会根据根目录的 `pyproject.toml` 和 `uv.lock` 使用已锁定的依赖版本。

## 启动 HTTP API

### 无 Provider 配置

```bash
pnpm dev:api
```

没有 `apps/api/.env` 时，Health 和 Provider Catalog 仍可使用；Chat 请求会安全返回 `503`。

### 本地真实 Provider 配置

先根据 `apps/api/.env.example` 创建被 Git 忽略的 `apps/api/.env`，只填写需要使用的 Provider：

```dotenv
AI_PROVIDER_API_KEY=
AI_PROVIDER_BASE_URL=

AI_PROVIDER_OPENROUTER_API_KEY=
AI_PROVIDER_OPENROUTER_BASE_URL=
```

`pnpm dev:api` 会在该文件存在时通过 `uv run --env-file` 加载配置。修改 Key 后需要重启 API；Key 只进入 FastAPI 进程，不会由 `GET /providers`、HTTP 错误或 Web 页面返回。生产环境应由部署平台的 Secret Manager 注入，不使用本地 `.env`。

Day 26 的 `Settings` 会从环境变量读取 `JACK_ENVIRONMENT`、`JACK_API_HOST`、`JACK_API_PORT`、`JACK_DATABASE_URL` 和 `JACK_REDIS_URL`，并在 API 进程启动边界校验类型、范围和允许值。配置本身不建立 PostgreSQL 或 Redis 网络连接；Day 27 在此基础上加入数据库 Engine 和 Session 边界。

Day 27 的 `get_database_engine()` 只在第一次需要数据库依赖时创建 Engine；`get_db_session()` 为每个请求提供独立 Session，异常时回滚并在请求结束后关闭。没有 `JACK_DATABASE_URL` 时会明确报告数据库未配置，不会伪造可用连接。

启动后访问：

- Health Endpoint：`http://127.0.0.1:8000/health`
- Provider Catalog：`http://127.0.0.1:8000/providers`
- Chat Endpoint（POST）：`http://127.0.0.1:8000/chat`
- Streaming Chat Endpoint（POST）：`http://127.0.0.1:8000/chat/stream`
- OpenAPI 文档：`http://127.0.0.1:8000/docs`

`POST /chat` 与 `POST /chat/stream` 的 `output_mode` 支持 `text` 和 `structured_answer`。结构化模式会向 OpenAI-compatible Provider 请求 JSON Schema，并在 API 服务端使用 `StructuredAnswer` 校验最终内容。自动化测试继续使用 Fake Provider；真实 Provider 只在显式配置本地 Key 后调用。

## 自动化测试

在仓库根目录执行：

```bash
pnpm test:api
```

当前测试覆盖 Health 路由函数与注册契约，以及 Chat Message Role、非空消息和 Temperature 范围等运行时数据边界。单元测试不代替真实 HTTP 联调。

Day 12 的 Provider 单元测试使用 Mock Client。Day 13 的 HTTP 测试通过 FastAPI Dependency Override 使用 Fake Provider，覆盖成功响应、`422` 请求校验、`502` Provider 无效响应和 `503` 配置缺失。Day 14 的 Fake Stream 测试覆盖多个文本分片、空分片、`delta`、`done` 和流内安全 `error`。Day 16 的 Provider Registry 测试覆盖安全 Catalog、独立环境变量和未配置 Provider。Day 18 的测试覆盖输出模式、JSON Schema 请求参数、非流式/流式结构校验和无效结构错误。Day 19～24 的测试继续覆盖严格 Tool Call、Executor、Tool Result 关联、一次 Follow-up 和 HTTP 编排。这些自动化测试都不读取真实 Key、不请求外部模型，也不消耗 Provider 额度；Day 25 另行记录显式真实调用证据。

## 计划职责

- 保护模型 Provider 的 API Key。
- 统一处理模型调用、业务规则和错误。
- 提供用户、会话、RAG、Agent、MCP 与 Workflow API。
- 记录日志、用量和工具调用审计信息。
