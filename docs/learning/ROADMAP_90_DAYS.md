# Jack AI Studio 90 天学习路线图

## 训练目标

在 90 天内，通过持续开发 Jack AI Studio，逐步掌握现代 AI 应用的设计、开发、测试与部署方法，最终完成可运行、可部署、可公开展示的 v1.0。

本路线图只定义阶段边界。每个 Day 的详细内容会在当天开始时，根据项目进度写入 `docs/learning/daily/day-XXX.md`，避免提前生成全部课程或脱离项目实际情况。

## 学习原则

- 项目驱动：所有知识尽量落到 Jack AI Studio。
- 小步迭代：每个 Day 聚焦一个明确目标，并形成一次清晰提交。
- 先理解后实现：先解释问题与方案，再修改代码。
- 按需学习：Python、React 和 AI 技术只学习当前阶段需要的部分。
- 流程可视化：每个 Day 只要涉及请求链路、数据流、执行顺序、生命周期或状态变化，就使用 Mermaid 流程图；流程图从上到下、按步骤编号并优先使用大白话，复杂流程拆图表达。
- 可验证：每天都要有明确的练习与验收标准。

## Sprint 1：项目启动与基础能力（Day 1～10）

### 目标

- 理解 AI 应用开发与基础 LLM（大语言模型）概念。
- 建立 React、Next.js 和 Python 的必要基础。
- 完成 Jack AI Studio 的基础框架。

### 阶段成果

- 项目可运行。
- 具备 Dashboard 和 Chat 页面骨架。
- 建立基础项目文档和第一批学习记录。

## Sprint 2：AI Chat（Day 11～25）

### 目标

- 接入大模型并实现流式输出。
- 支持 Markdown、多 Provider（模型服务提供方）和 Prompt Library（提示词库）。
- 学习 Structured Output（结构化输出）与 Tool Calling（工具调用）。

### 阶段成果

- 完成可用的 AI Chat V1。

## Sprint 3：后端与数据持久化（Day 26～35）

### 目标

- 学习 FastAPI、PostgreSQL 和 Redis。
- 实现用户、登录、会话、消息持久化、日志与测试。

### 阶段成果

- 建立完整的后端基础能力。

## Sprint 4：RAG 知识库（Day 36～52）

### 目标

- 实现文档上传、解析、切分、向量化和检索。
- 学习 pgvector、Rerank（重排序）、Citation（引用）和 RAG 评估。

### 阶段成果

- 完成 Knowledge Center（知识中心）。
- 支持可溯源的知识库问答。

## Sprint 5：Agent 与 Memory（Day 53～66）

### 目标

- 学习 Agent（智能体）、ReAct、State（状态）与 Tool Registry（工具注册表）。
- 实现 Memory（记忆）、Human in the Loop（人工介入）和 Agent 评估。

### 阶段成果

- 完成 Agent Center。
- 支持查看执行步骤、调用工具和人工确认。

## Sprint 6：MCP（Day 67～76）

### 目标

- 学习 MCP Host、Client、Server、Tool 和 Resource。
- 实现权限管理和调试面板。

### 阶段成果

- 完成 MCP Center。
- 支持连接多个 MCP Server。

## Sprint 7：Workflow（Day 77～84）

### 目标

- 学习 DAG（有向无环图）、节点、条件和变量。
- 实现 Workflow Executor（工作流执行器）、可视化编排、重试和恢复。

### 阶段成果

- 完成可视化 Workflow Builder。

## Sprint 8：产品化与发布（Day 85～90）

### 目标

- 完成安全、Docker、CI/CD、日志、监控与文档建设。
- 完成开源和公开发布准备。

### 阶段成果

- 发布 Jack AI Studio v1.0。

## 进度维护

- 当前进度以 `docs/learning/PROGRESS.md` 为准。
- 每天只在开始当天任务时创建对应的 daily 文档。
- 完成一个 Day 后，更新进度、验收结果和下一步。
