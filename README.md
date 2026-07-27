# Jack AI Studio

Jack AI Studio 是一个面向开发者的 AI Workspace，也是一个 90 天 AI 全栈工程师训练项目。

## 当前状态

项目正在进行 Sprint 1，目前已建立最小 pnpm workspace、Next.js Web 应用骨架，以及零第三方依赖的 Python API 程序入口。当前 Python 程序只用于基础学习和终端验证，尚未提供 HTTP API。

## 目录

```text
apps/
├── web/  # Next.js Web 应用
└── api/  # Python API 服务（当前为最小程序入口）
```

## 本地开发

环境要求：

- Node.js 22+
- pnpm 10.28.1
- Python 3.12+（后续 API 开发使用）

安装依赖并启动 Web 应用：

```bash
pnpm install
pnpm dev:web
```

常用验证命令：

```bash
pnpm lint:web
pnpm build:web
.venv/bin/python apps/api/app/main.py
```

学习进度以 [`docs/learning/PROGRESS.md`](docs/learning/PROGRESS.md) 为准。
