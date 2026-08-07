# 当前学习进度

- 当前 Sprint：Sprint 2 · AI Chat
- 当前 Day：Day 19 · 已完成
- 当前日期：2026-08-07
- 已完成：Day 1～19；Sprint 1 阶段总结已补充至 `docs/learning/sprint-01-summary.md`；Day 19 已完成服务端 Tool Definition、Raw/Validated Tool Call、allowlist、Pydantic 严格参数校验、完整质量门禁、API 44 个测试、Python 正常/异常运行演示、桌面端与 `390×844` 移动端页面回归及五道核心概念问答
- 未完成：Day 20 尚未开始
- 当前项目状态：Web 继续支持 Provider Catalog、Prompt Library、SSE Streaming、安全 Markdown 和 Structured JSON 展示；Day 19 仅在 API 内新增 `add_numbers` Tool Definition 与参数校验，尚未接入 Provider、Route 或 Web，不执行工具
- 当前分支：`develop`
- 最近一次 Commit：`feat(tools): add tool calling contract for day 19`（当前 HEAD）
- 遇到的问题：已修正 Day 18 Commit 状态滞后；首次聚焦测试使用了错误 import 入口，改用项目既有 unittest discovery 后测试通过，源码无需修改；保留已有 Starlette `TestClient` deprecation warning
- 尚未理解：暂无；Day 19 已能区分 Tool Call 与工具执行、服务端能力所有权、Raw/Validated 数据，以及 allowlist 与 Pydantic 的不同职责
- 下一步：开始 Day 20 前重新读取路线图，确认 Provider Tool Call 接入的最小范围

## 更新规则

- 本文件是学习进度的唯一事实来源，不依赖聊天记录判断进度。
- 每完成一个 Day，都要记录完成项、遗留问题、当前项目状态和下一步。
- 每次更新应以实际代码、文档和验收结果为依据。
