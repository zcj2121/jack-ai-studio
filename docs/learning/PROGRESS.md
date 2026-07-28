# 当前学习进度

- 当前 Sprint：Sprint 1 · 项目启动与基础能力
- 当前 Day：Day 7 · 已完成
- 当前日期：2026-07-28
- 已完成：Day 1～7；Day 7 Pydantic、Runtime Validation、Schema、BaseModel、Field 与 ValidationError；可复现依赖管理；`ServiceStatus` 正常/错误数据验证；uv PATH 与 WebStorm 项目解释器配置；命令检查和核心概念问答验收
- 未完成：Day 8 尚未开始
- 当前项目状态：最小 Monorepo、Next.js Web 应用骨架和带 Pydantic 运行时校验的 Python 程序入口已建立；Python 程序仍不是 HTTP API；未接入 FastAPI、模型、API 或会话业务
- 当前分支：`develop`
- 最近一次 Commit：`feat(api): add Python foundation entry point for day 6`
- 遇到的问题：Codex 运行环境执行 `pnpm dev:web` 时出现 `EMFILE: too many open files, watch`，并导致 dev 首页返回 404；用户已确认本机开发服务器运行和访问均正常，因此该问题只存在于 Codex 受限运行环境
- 尚未理解：当前无遗留疑问；需继续保持“先校验外部数据，再进入业务逻辑”的数据边界意识
- 下一步：开始 Day 8 前读取本文件和 Day 7 总结，再根据当前项目状态确定最小学习与开发范围

## 更新规则

- 本文件是学习进度的唯一事实来源，不依赖聊天记录判断进度。
- 每完成一个 Day，都要记录完成项、遗留问题、当前项目状态和下一步。
- 每次更新应以实际代码、文档和验收结果为依据。
