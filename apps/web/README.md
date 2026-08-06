# Jack AI Studio Web

这里是 Jack AI Studio 的 Next.js Web 应用。

Day 16 已增加最小多 Provider 闭环。Web 先通过统一 `getChatProviders()` 请求同源 `GET /api/providers`，取得 Provider 的安全元数据和配置状态；用户选择 Provider 后，`streamChatCompletion()` 会把 `provider`、`model` 和消息一起发送到 FastAPI。Provider Registry 根据稳定 ID 选择服务端环境变量，不会向浏览器返回 API Key 或 Base URL。

SSE 与 Markdown 链路保持不变。未配置 Provider API Key 时，可以点击 Chat 页面中的 `Markdown 演示`，使用本地分片观察标题、列表和代码块；该演示不会请求 API。

Provider API Key 不进入 Web 环境变量或浏览器 JavaScript，只由 FastAPI 服务端读取。

## 本地开发

在仓库根目录分别启动 API 与 Web：

```bash
pnpm dev:api
pnpm dev:web
```

访问：

- 首页：`http://127.0.0.1:3000`
- Chat Workspace：`http://127.0.0.1:3000/chat`

复制 `.env.example` 为本地 `.env.local` 后，可以修改 Next.js 服务端访问 FastAPI 的地址：

```text
API_BASE_URL=http://127.0.0.1:8000
```

不要把 Provider API Key 写入 `NEXT_PUBLIC_` 变量。

## 当前边界

- SSE 流式单轮 Chat 请求；保留 Day 13 非流式请求封装作为兼容路径。
- Provider Catalog 当前包含 `openai-compatible` 与 `openrouter`，两者共享 OpenAI-compatible Adapter。
- 页面消息只保存在 React State，刷新后清空。
- 当前没有请求取消、会话持久化、多轮上下文或 Provider 管理后台。
- 未配置所选 Provider 时，页面显示配置状态并禁用真实流式发送。

## 验证

```bash
pnpm check:web
```
