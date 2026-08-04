# Jack AI Studio Web

这里是 Jack AI Studio 的 Next.js Web 应用。

Day 13 已启用 Chat Workspace 的 Model 与 Prompt 输入。浏览器通过统一 `createChatCompletion()` 请求同源 `POST /api/chat`，Next.js Route Handler 再使用服务端 `API_BASE_URL` 转发到 FastAPI `POST /chat`。

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

- 非流式单轮 Chat 请求。
- 页面消息只保存在 React State，刷新后清空。
- 当前没有会话持久化、多轮上下文或 Markdown 渲染。
- 未配置 FastAPI Provider Key 时，页面显示 `503` 对应的中文提示。

## 验证

```bash
pnpm check:web
```
