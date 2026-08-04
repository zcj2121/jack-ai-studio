# Jack AI Studio Web

这里是 Jack AI Studio 的 Next.js Web 应用。

Day 14 已把 Chat Workspace 升级为 SSE Streaming。浏览器通过统一 `streamChatCompletion()` 请求同源 `POST /api/chat/stream`，Next.js Route Handler 使用服务端 `API_BASE_URL` 转发到 FastAPI `POST /chat/stream`，并直接透传 Response Body。Web 每收到一个 `delta` Event 就追加 Assistant Message。

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
- 页面消息只保存在 React State，刷新后清空。
- 当前没有请求取消、会话持久化、多轮上下文或 Markdown 渲染。
- 未配置 FastAPI Provider Key 时，页面显示 `503` 对应的中文提示。

## 验证

```bash
pnpm check:web
```
