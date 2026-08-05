# 当前学习进度

- 当前 Sprint：Sprint 2 · AI Chat
- 当前 Day：Day 15 · 已完成
- 当前日期：2026-08-05
- 已完成：Day 1～15；Day 15 已新增 `MarkdownMessage` 和无需 API Key 的 `Markdown 演示`，Assistant Message 支持标题、列表、引用、代码和链接的安全 Markdown 展示，真实 API 与 SSE 请求链路保持不变；Web Lint、TypeScript、Production Build、API 20 个回归测试、桌面/移动端浏览器验收和概念问答均已通过
- 未完成：Day 16 尚未开始
- 当前项目状态：Web 已通过同源 `/api/chat/stream` 连接 FastAPI 与 Provider Adapter，可逐段展示并排版单轮 Assistant 回答；本地 Markdown 演示无需 API Key；真实 Provider 仍未配置、未调用真实模型、未持久化会话
- 当前分支：`develop`
- 最近一次 Commit：`c5fa4d5 feat(chat): add SSE streaming for day 14`
- 遇到的问题：SSE Event 与网络 Chunk 边界不一致，Web 已使用 Buffer 处理；流开始后无法修改 HTTP Status Code，已使用安全 `event: error` 表达流内失败；已有 Starlette `TestClient` deprecation warning 暂不阻塞
- 尚未理解：当前无遗留疑问；需要继续巩固网络 Chunk 与 SSE Event 的边界、读取完整 Response 与透传 Stream 的区别，以及原始 HTML 解析与 XSS 风险的关系
- 下一步：读取路线图并开始 Day 16

## 更新规则

- 本文件是学习进度的唯一事实来源，不依赖聊天记录判断进度。
- 每完成一个 Day，都要记录完成项、遗留问题、当前项目状态和下一步。
- 每次更新应以实际代码、文档和验收结果为依据。
