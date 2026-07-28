# Jack AI Studio API

这里将存放 Jack AI Studio 的 Python API 服务。

Day 6 已建立 Python 程序入口。Day 7 在此基础上引入 Pydantic，用 `BaseModel` 和 `Field` 定义服务状态 Schema，并在运行时拒绝不符合约束的数据。

当前入口仍然只会在终端输出正常校验结果和错误数据演示，不是 HTTP API，也不会启动端口。后续进入 Python Web API 学习时，再按当天范围引入 FastAPI。

## 运行

在仓库根目录执行：

```bash
uv run python apps/api/app/main.py
```

`uv` 会根据根目录的 `pyproject.toml` 和 `uv.lock` 使用已锁定的依赖版本。

## 计划职责

- 保护模型 Provider 的 API Key。
- 统一处理模型调用、业务规则和错误。
- 提供用户、会话、RAG、Agent、MCP 与 Workflow API。
- 记录日志、用量和工具调用审计信息。
