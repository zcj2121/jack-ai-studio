# Jack AI Studio API

这里将存放 Jack AI Studio 的 Python API 服务。

Day 6 已建立零第三方依赖的 Python 程序入口，用于学习 Module、Function、list、dict、Type Hints 和 `__main__` 入口判断。

当前入口只会在终端输出服务状态，不是 HTTP API，也不会启动端口。后续进入 Python Web API 学习时，再按当天范围引入 FastAPI。

## 运行

在仓库根目录执行：

```bash
.venv/bin/python apps/api/app/main.py
```

## 计划职责

- 保护模型 Provider 的 API Key。
- 统一处理模型调用、业务规则和错误。
- 提供用户、会话、RAG、Agent、MCP 与 Workflow API。
- 记录日志、用量和工具调用审计信息。
