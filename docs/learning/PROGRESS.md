# 当前学习进度

- 当前 Sprint：Sprint 2 · AI Chat
- 当前 Day：Day 24 · 已完成
- 当前日期：2026-08-26
- 已完成：Day 1～24；Sprint 1 阶段总结已补充至 `docs/learning/sprint-01-summary.md`；Day 24 已新增固定单轮 Chat Orchestrator，将 Provider Tool Call、Executor、Follow-up 和 ChatMessage 串入非流式 `/chat`，Web 已接入“流式对话 / 工具调用”请求模式；Web lint/typecheck/build、Python 编译、60 个 API 测试、桌面和移动端浏览器验收及五道核心概念问答通过
- 未完成：Day 25 尚未开始；真实 API Key 与真实模型端到端链路尚未验收；Sprint 2 总结和复习问答尚未完成
- 当前项目状态：Web 支持 Provider Catalog、Prompt Library、安全 Markdown、Structured JSON、SSE 流式对话和非流式工具调用模式，首页进度标识已同步 Day 24；API `/chat` 可完成一次 Tool Calling HTTP 闭环，`/chat/stream` 仍只处理文本 SSE；不执行多轮 Agent Loop，Agent/MCP/数据库能力未实现
- 当前分支：`develop`
- 最近一次 Commit：`feat(provider): add single tool follow-up for day 23`（`42864db`，当前 HEAD）
- 遇到的问题：Tool Calling 与现有 Web SSE 协议不同；Day 24 使用独立的非流式工具模式复用 `/api/chat`，保留文本 SSE 行为；Next dev 浏览器验收需使用 `localhost` 保持同源，`127.0.0.1` 会触发 dev resource origin 限制；当前无真实 API Key，使用 Fake Provider 验证完整 HTTP 工具闭环；保留已有 Starlette `TestClient` deprecation warning
- 尚未理解：暂无；Day 24 已能说明 Application Service 的隔离作用、SSE 与普通 HTTP 的差异、运行时校验和 Agent Loop 的必要控制，并已修正“Tool Call 由 Web 传入”的误解，明确 Tool Call 来自 Provider/LLM 响应
- 下一步：开始 Day 25，通过服务端环境变量配置真实 API Key，完成 AI Chat V1 的真实模型端到端验收、Sprint 2 总结和复习问答

## 更新规则

- 本文件是学习进度的唯一事实来源，不依赖聊天记录判断进度。
- 每完成一个 Day，都要记录完成项、遗留问题、当前项目状态和下一步。
- 每次更新应以实际代码、文档和验收结果为依据。
