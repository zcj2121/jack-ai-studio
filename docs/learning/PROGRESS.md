# 当前学习进度

- 当前 Sprint：Sprint 2 · AI Chat
- 当前 Day：Day 20 · 已完成
- 当前日期：2026-08-25
- 已完成：Day 1～20；Sprint 1 阶段总结已补充至 `docs/learning/sprint-01-summary.md`；Day 20 已完成服务端 Tool Definition 接入 Provider、Provider `tool_calls` 解析、Validated Tool Call、47 个 API 测试、Web lint/typecheck/build、Python 编译检查、运行时演示和五道核心概念问答
- 未完成：Day 21 尚未开始
- 当前项目状态：Web 继续支持 Provider Catalog、Prompt Library、SSE Streaming、安全 Markdown 和 Structured JSON 展示；Day 20 已在 API Provider 内附加服务端 `add_numbers` Tool Definition，并将合法 `tool_calls` 转换为 `ValidatedToolCall`，暂不执行工具、不发起第二次模型请求，Web 和 SSE 文本契约保持不变
- 当前分支：`develop`
- 最近一次 Commit：`feat(tools): add tool calling contract for day 19`（当前 HEAD）
- 遇到的问题：Provider 普通文本响应没有 `tool_calls`，需要兼容可选字段；现有 Web 文本契约不能直接展示工具请求，因此本日保留 Provider 内部结果并在 `generate()` 处停止；`pnpm check:foundation` 和 47 个 API 测试已通过；保留已有 Starlette `TestClient` deprecation warning
- 尚未理解：暂无；Day 20 已能区分服务端 `tools`、Provider `tool_calls`、Validated Tool Call、验证层与执行控制流
- 下一步：开始 Day 21；工具执行、Tool Result、第二次模型请求和 Agent Loop 仍未提前实现

## 更新规则

- 本文件是学习进度的唯一事实来源，不依赖聊天记录判断进度。
- 每完成一个 Day，都要记录完成项、遗留问题、当前项目状态和下一步。
- 每次更新应以实际代码、文档和验收结果为依据。
