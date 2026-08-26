# Jack AI Studio

Jack AI Studio 是一个面向开发者的 AI Workspace，也是一个 90 天 AI 全栈工程师训练项目。

## 当前状态

Sprint 1 与 Sprint 2 已完成，Sprint 3 Day 26 待开始。目前已建立基础框架、前后端 Health 联通、统一质量门禁、AI Chat 消息契约、OpenAI-compatible Provider Adapter、`text` / `structured_answer` 输出模式，以及 Web → Next.js Route Handler → FastAPI 的 Chat 请求链路。Web 支持 SSE 流式对话和固定单轮 Tool Calling：非流式 `/chat` 可在 Provider 请求工具时执行服务端 `add_numbers`，回传 Tool Result，并展示最终 Assistant Message。Text、SSE、Structured Output 和 Tool Calling 已通过一次显式第三方 OpenAI-compatible Provider 真实验收；当前不支持流式 Tool Calling、多轮 Agent Loop 或数据持久化，后端与数据能力从 Day 26 开始建设。

## 目录

```text
apps/
├── web/  # Next.js Web 应用
└── api/  # Python API 服务（当前为最小程序入口）
```

## 本地开发

环境要求：

- Node.js 22+
- pnpm 10.28.1
- Python 3.12+
- uv 0.11+（Python 环境与依赖管理）

安装依赖：

```bash
pnpm install
uv sync
```

分别在两个终端启动 API 与 Web：

```bash
pnpm dev:api
pnpm dev:web
```

访问：

```text
Web：http://127.0.0.1:3000
API Health：http://127.0.0.1:8000/health
API Chat（POST）：http://127.0.0.1:8000/chat
API Streaming Chat（POST）：http://127.0.0.1:8000/chat/stream
API Docs：http://127.0.0.1:8000/docs
```

运行 Sprint 1 基础质量门禁：

```bash
pnpm check:foundation
```

该命令会依次执行 Web ESLint、TypeScript、生产构建，以及 Python 依赖锁、语法编译和 Health 自动化测试。任一步骤失败都会返回非零 Exit Code。

学习进度以 [`docs/learning/PROGRESS.md`](docs/learning/PROGRESS.md) 为准。
