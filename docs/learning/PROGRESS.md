# 当前学习进度

- 当前 Sprint：Sprint 2 · AI Chat
- 当前 Day：Day 16 · 已完成
- 当前日期：2026-08-06
- 已完成：Day 1～16；Day 16 已实现 `openai-compatible` 与 `openrouter` 的 Provider Registry、`GET /providers` 安全目录、`ChatRequest.provider` 契约，以及 Web Provider Loading/Configured/Unconfigured/Error 状态；完整质量门禁、API 28 个测试、桌面端与 `390×844` 移动端浏览器验收、核心概念问答均已通过
- 未完成：Day 17 尚未开始
- 当前项目状态：Web 通过同源 `/api/providers` 获取 Provider 安全元数据，并通过 `/api/chat/stream` 携带稳定 Provider ID；两个 Provider 共用 OpenAI-compatible Adapter，API Key 与 Base URL 只在 FastAPI 服务端；本地 Markdown 演示无需 API Key，尚未调用真实模型或持久化会话
- 当前分支：`develop`
- 最近一次 Commit：`e51bf50 feat(provider): add multi-provider selection for day 16`
- 遇到的问题：移动端 Markdown 代码块一度通过 Grid/Flex 最小内容宽度把页面撑到 `483px`，已使用 `min-w-0` 修复并复验为 `390px`；已有 Starlette `TestClient` deprecation warning 暂不阻塞
- 尚未理解：当前无 Day 16 遗留疑问；已补充 Registry/Adapter 分工、Catalog 快照与 API 双重校验、稳定 ID 和 Adapter 复用边界
- 下一步：开始 Day 17；根据当前 Multi-provider Chat 基线确定当天范围，不提前开发

## 更新规则

- 本文件是学习进度的唯一事实来源，不依赖聊天记录判断进度。
- 每完成一个 Day，都要记录完成项、遗留问题、当前项目状态和下一步。
- 每次更新应以实际代码、文档和验收结果为依据。
