# 当前学习进度

- 当前 Sprint：Sprint 1 · 项目启动与基础能力
- 当前 Day：Day 8 · 已完成
- 当前日期：2026-07-28
- 已完成：Day 1～8；Day 8 FastAPI、Uvicorn、HTTP Request/Response、Endpoint、GET、JSON、ASGI 与 Decorator；`GET /health`、真实 HTTP 200/404、Swagger UI 交互和核心概念问答验收
- 未完成：Day 9 尚未开始
- 当前项目状态：最小 Monorepo、Next.js Web 应用骨架和 FastAPI Health Endpoint 已建立；未接入模型、数据库、用户、会话或其他业务 API
- 当前分支：`develop`
- 最近一次 Commit：`feat(api): add Pydantic runtime validation for day 7`
- 遇到的问题：Codex 运行环境执行 `pnpm dev:web` 时出现 `EMFILE: too many open files, watch`，并导致 dev 首页返回 404；用户已确认本机开发服务器运行和访问均正常，因此该问题只存在于 Codex 受限运行环境
- 尚未理解：当前无遗留疑问；需继续区分 Uvicorn 的网络 Server 职责与 FastAPI 的 Application 职责
- 下一步：开始 Day 9 前读取本文件和 Day 8 总结，再根据当前项目状态确定最小学习与开发范围

## 更新规则

- 本文件是学习进度的唯一事实来源，不依赖聊天记录判断进度。
- 每完成一个 Day，都要记录完成项、遗留问题、当前项目状态和下一步。
- 每次更新应以实际代码、文档和验收结果为依据。
