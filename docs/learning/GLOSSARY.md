# Jack AI Studio 术语表

本术语表随训练进度增量维护，只收录已经学习或当前任务需要的概念。首次收录时包含专业解释、大白话、例子和项目用途。

## 1. AI Application（AI 应用）

**专业解释：** 将 AI 模型、业务逻辑、数据和用户界面组合起来解决实际问题的软件系统。

**大白话：** 模型只是“发动机”，AI 应用是包含方向盘、车轮和安全系统的“整辆车”。

**举例：** Jack AI Studio 的 Chat 不仅生成回答，还要管理会话、权限、错误和用量。

**项目用途：** Jack AI Studio 本身就是要长期建设的 AI Application。

## 2. Large Language Model（LLM，大语言模型）

**专业解释：** 基于海量文本训练、能够理解和生成自然语言的神经网络模型。

**大白话：** 可以先理解为 AI 的“语言大脑”。

**举例：** 模型可以根据“用 Vue 类比 React”生成一段新的解释。

**项目用途：** 是 Chat、RAG 和 Agent 的模型基础。

## 3. Prompt（提示词）

**专业解释：** 发送给模型的指令、背景、上下文和输出约束。

**大白话：** 给 AI 的任务说明书。

**举例：** 指定“使用中文、列出 3 点、附代码”比只说“解释泛型”更清楚。

**项目用途：** Chat 使用 Prompt 发起请求，Prompt Library 负责保存和复用它。

## 4. Token（词元）

**专业解释：** 模型处理文本时使用的基本计算单位。

**大白话：** AI 数字世界里的“字数”，但不严格等于汉字或单词数量。

**举例：** “今天天气不错。”在不同模型中可能被拆成不同数量的 Token。

**项目用途：** 影响上下文长度、响应速度和模型费用。

## 5. Context Window（上下文窗口）

**专业解释：** 模型单次请求能够处理的输入与输出 Token 总量范围。

**大白话：** AI 的有限办公桌，所有指令、消息和回答都要放在桌面上。

**举例：** 对话太长时，需要删除旧消息、生成摘要或只检索相关内容。

**项目用途：** 约束会话历史、Memory 和 RAG 的设计。

## 6. Inference（推理）

**专业解释：** 使用已经训练好的模型，根据输入计算并生成结果的过程。

**大白话：** 训练是上学，推理是学完后现场答题。

**举例：** 用户发送问题，模型生成回答，就是一次推理。

**项目用途：** Jack AI Studio 负责调用和管理推理，不负责训练基础模型。

## 7. Provider（模型服务提供方）

**专业解释：** 通过 API 提供模型访问、鉴权和计费能力的服务方。

**大白话：** 像云服务器厂商，模型是它提供给你使用的一项云能力。

**举例：** 不同 Provider 可能提供不同模型、价格、限流规则和请求格式。

**项目用途：** 项目未来会通过统一适配层连接多个 Provider。

## 8. API（Application Programming Interface，应用程序编程接口）

**专业解释：** 软件系统之间交换数据和调用能力的一组约定。

**大白话：** 像餐厅的点餐窗口，你按菜单格式提交需求，后厨按约定返回结果。

**举例：** 后端向模型 API 发送 Prompt，再接收模型生成的回答。

**项目用途：** 连接前端、后端、模型服务和未来的外部工具。

## 9. Frontend（前端）

**专业解释：** 在用户设备上运行，负责交互、状态展示和请求发起的应用层。

**大白话：** 用户能够看到和操作的“店面”。

**举例：** Chat 输入框、消息列表和 Dashboard 都属于前端。

**项目用途：** 提供 Jack AI Studio 的 Web 用户界面。

## 10. Backend（后端）

**专业解释：** 运行在可信服务器环境中，负责业务逻辑、数据访问、安全和外部服务编排的应用层。

**大白话：** 用户看不到的“后厨”，负责真正处理订单，并保管不能公开的东西。

**举例：** 后端保存 API Key，调用模型并把会话写入数据库。

**项目用途：** 保护密钥，统一处理模型调用、数据、日志、权限和错误。

## 11. Monorepo（单仓库多项目）

**专业解释：** 在同一个 Git 仓库中管理多个相关应用或包的代码组织方式。

**大白话：** 多个项目住在同一个小区，共享仓库历史和工程规范，但各自仍有独立职责。

**举例：** `apps/web` 管理 Web 界面，`apps/api` 管理 Python API。

**项目用途：** 统一管理 Jack AI Studio 的前端、后端和未来共享包。

## 12. Workspace（工作区）

**专业解释：** 包管理器对单仓库内多个包进行统一依赖安装和脚本调度的能力。

**大白话：** 像 Monorepo 的物业系统，能统一找到和管理每个应用。

**举例：** pnpm 可以通过包名只对 `@jack-ai-studio/web` 执行 build。

**项目用途：** 根目录使用 pnpm workspace 统一管理 JavaScript 和 TypeScript 包。

## 13. App Router（应用路由器）

**专业解释：** Next.js 基于 `app` 目录组织页面、布局和服务端组件的路由系统。

**大白话：** 类似通过文件目录自动生成 Vue Router 路由配置。

**举例：** `app/page.tsx` 对应 `/` 首页。

**项目用途：** 后续用于组织 Dashboard、Chat、Knowledge 和 Agent 等 Web 页面。

## 14. Build（构建）

**专业解释：** 将源代码经过编译、类型检查和优化，生成可部署产物的过程。

**大白话：** 把开发时的源码加工成服务器真正要运行的成品。

**举例：** `pnpm build:web` 会检查并构建 Next.js 页面。

**项目用途：** 用于验证 Web 应用能够生成生产版本，并为后续部署做准备。

## 15. Component（组件）

**专业解释：** 封装界面结构、样式和行为的可复用 UI 单元。

**大白话：** 像 Vue 组件一样，把复杂页面拆成职责明确的小积木。

**举例：** `FeatureCard` 使用同一套结构展示不同产品模块。

**项目用途：** 用于组织首页、Chat 消息、表单和未来各业务界面。

## 16. JSX（JavaScript 语法扩展）

**专业解释：** 允许在 JavaScript 或 TypeScript 中编写类似 HTML 的声明式 UI 语法。

**大白话：** 类似 Vue Template，但它直接写在 React 函数的返回值中。

**举例：** `<h2>{title}</h2>` 会展示变量 `title` 的值。

**项目用途：** React 组件通过 JSX 描述 Jack AI Studio 的界面结构。

## 17. Props（属性参数）

**专业解释：** 父组件传给子组件的只读输入。

**大白话：** 与 Vue Props 类似，用数据配置同一个组件的不同内容。

**举例：** 首页把 `title`、`description` 和 `status` 传给 `FeatureCard`。

**项目用途：** 建立组件之间清晰、类型安全的数据契约。

## 18. State（状态）

**专业解释：** 组件内部会随事件变化，并驱动界面重新渲染的数据。

**大白话：** `useState` 可以先类比 Vue 的 `ref`，但更新时需要调用 setter 函数。

**举例：** 点击按钮更新 `activeView`，说明文字随之改变。

**项目用途：** 管理输入框、选择器、弹窗和其他局部交互状态。

## 19. Hydration（水合）

**专业解释：** React 在浏览器中为服务端生成的 HTML 绑定事件和客户端状态，使其可以交互的过程。

**大白话：** 服务器先搭好静态舞台，浏览器再接上按钮和机关。

**举例：** `WorkspaceViewToggle` 的 HTML 可以先展示，Hydration 后按钮点击才能更新 State。

**项目用途：** Next.js 用它让预渲染页面中的 Client Component 具备交互能力。

## 20. Event（事件）

**专业解释：** 浏览器对点击、输入、提交等用户操作的结构化描述。

**大白话：** 用户做了一个动作，组件收到通知后决定如何处理。

**举例：** 文本域内容变化时，`onChange` 处理函数可以读取新的输入值。

**项目用途：** 用于处理 Prompt 输入、消息发送、Provider 选择和其他用户操作。

## 21. Controlled Component（受控组件）

**专业解释：** 当前值由 React State 控制，并通过事件更新 State 的表单组件。

**大白话：** State 是唯一账本，输入框只负责展示账本内容并报告变化。

**举例：** `value={prompt}` 展示当前 State，`onChange` 调用 `setPrompt` 更新它。

**项目用途：** 让 Prompt 内容、校验和按钮状态来自同一份可靠数据。

## 22. Unidirectional Data Flow（单向数据流）

**专业解释：** 数据从 State 流向 UI，事件再触发 State 更新的数据流动方式。

**大白话：** 数据按固定方向传递，每次变化都能找到来源，不让界面和变量彼此偷偷修改。

**举例：** `prompt State → textarea → onChange → setPrompt → 新 State`。

**项目用途：** 让 Chat 输入、发送状态和校验逻辑更容易理解与调试。

## 23. Derived State（派生状态）

**专业解释：** 能够根据现有 State 直接计算得到、无需重复保存的数据。

**大白话：** 已有单价和数量时，总价现场计算即可，不再维护第二本账。

**举例：** `canSubmit` 根据去除空白后的 Prompt 长度计算。

**项目用途：** 用于按钮禁用、字数、过滤结果和其他可计算的界面状态。

## 24. Route（路由）

**专业解释：** URL 与应用页面内容之间的映射规则。

**大白话：** 根据用户访问的地址，找到应该展示的页面。

**举例：** `/chat` 对应 `app/chat/page.tsx`。

**项目用途：** 用于组织首页、Chat、Knowledge 和 Agent Center 等产品页面。

## 25. File-system Routing（文件系统路由）

**专业解释：** 使用目录和特定文件约定自动生成路由的机制。

**大白话：** 不写集中路由表，通过文件放在哪里决定页面地址。

**举例：** `app/chat/page.tsx` 自动暴露 `/chat` 页面。

**项目用途：** Jack AI Studio Web 端使用它建立清晰的产品页面结构。

## 26. Route Segment（路由片段）

**专业解释：** URL 中由 `/` 分隔的一段路径，在 App Router 中通常对应一个文件夹。

**大白话：** URL 像目录地址，每一级文件夹就是其中一段。

**举例：** `/chat` 中的 `chat` 是一个 Route Segment。

**项目用途：** 用于隔离 Chat 等模块的页面边界。

## 27. Client-side Navigation（客户端导航）

**专业解释：** 浏览器不重新加载整份文档，而是在客户端更新路由和页面内容的导航方式。

**大白话：** 页面切换时只更换需要变化的区域，不把整个应用重新启动一次。

**举例：** Next.js `<Link href="/chat">` 可以从首页切换到 Chat 页面。

**项目用途：** 让 Jack AI Studio 内部页面导航更快速、连贯。

## 28. Prefetch（预取）

**专业解释：** 在用户真正导航前，提前获取可能需要的页面资源。

**大白话：** 像进入下一间房前，先把灯打开。

**举例：** Next.js 可以在链接进入视口时预取静态路由资源。

**项目用途：** 缩短用户打开 Chat 等内部页面时的等待时间。

## 29. Module（模块）

**专业解释：** Python Module 通常是一个 `.py` 文件，用于组织可导入、可复用的变量、函数和类型。

**大白话：** 它类似 TypeScript 的 `.ts` 文件，是拆分和管理代码的基本单位。

**举例：** `apps/api/app/main.py` 是 Day 6 创建的程序入口模块。

**项目用途：** 后续用于拆分 API 路由、业务服务、Provider、RAG 和 Agent 等后端职责。

## 30. Type Hints（类型提示）

**专业解释：** Type Hints 描述 Python 变量、函数参数和返回值的预期类型，供开发工具和静态检查器分析。

**大白话：** 它类似 TypeScript 类型标注，但 Python 默认不会在运行时全面强制检查。

**举例：** `def main() -> None` 表示函数不返回业务数据。

**项目用途：** 用于明确 API Schema、服务层和 Provider 接口的数据契约。

## 31. Entry Point（程序入口）

**专业解释：** Entry Point 是程序开始执行的约定位置。Python 可通过 `if __name__ == "__main__"` 区分直接执行与模块导入。

**大白话：** 只有直接运行文件时才按下启动按钮，其他文件导入它时不会自动启动。

**举例：** 运行 `main.py` 会调用 `main()` 并输出服务状态。

**项目用途：** Day 6 用它验证 Python 程序；后续真正的 API Server 会有独立启动方式。

## 32. Runtime Validation（运行时校验）

**专业解释：** 程序执行期间检查实际输入是否满足类型、必填项和业务约束。

**大白话：** Type Hints 像表单字段旁的填写说明，Runtime Validation 像真正点击提交时执行的校验规则。

**举例：** 服务名称为空、计划能力列表为空时，Pydantic 在程序运行期间拒绝创建 `ServiceStatus`。

**项目用途：** 后续用于保护 API、模型配置、会话消息和工具调用的数据边界。

## 33. Pydantic

**专业解释：** Pydantic 是使用 Python Type Hints 定义数据模型，并执行数据解析、运行时校验和序列化的库。

**大白话：** 它类似 TypeScript 类型加 Zod 运行时校验的组合。

**举例：** `ServiceStatus.model_validate(raw_data)` 把普通 `dict` 校验成可信模型。

**项目用途：** 它会作为 Jack AI Studio 后端的 Schema 基础，并在后续与 FastAPI 配合校验请求和响应。

## 34. Schema（数据结构契约）

**专业解释：** Schema 描述一组数据有哪些字段、字段类型是什么，以及必须满足哪些约束。

**大白话：** 它像前后端共同遵守的表单说明书，不符合说明的数据不能进入下一步。

**举例：** `ServiceStatus` 要求名称、状态和 Python 版本非空，且至少包含一项计划能力。

**项目用途：** 用于约束 API 输入输出、Provider 配置、Chat Message 和后续 Agent State。

## 35. ValidationError（校验错误）

**专业解释：** Pydantic 在输入无法通过模型校验时抛出的异常，包含失败字段、错误类型和输入信息。

**大白话：** 它不是只说“表单错了”，而是会指出哪个字段违反了哪条规则。

**举例：** 空的 `name` 和 `planned_capabilities` 会产生对应字段的错误记录。

**项目用途：** 后续 API 会把校验问题转换为可理解的错误响应，并避免无效数据进入业务层。

## 36. HTTP（超文本传输协议）

**专业解释：** HTTP 是客户端与服务器交换 Request 和 Response 的应用层协议。

**大白话：** 它像前端和后端共同遵守的寄件格式，规定请求送到哪里、想做什么以及服务器如何回复。

**举例：** 浏览器向 `/health` 发送 GET Request，API 返回状态码 `200` 和 JSON Response。

**项目用途：** Jack AI Studio Web、未来第三方客户端和 Python API 通过 HTTP 通信。

## 37. FastAPI

**专业解释：** FastAPI 是基于 Python Type Hints、Starlette 和 Pydantic 构建的 ASGI Web Framework。

**大白话：** 它类似 Python 后端中的 Koa 加路由和运行时 Schema 集成。

**举例：** `app = FastAPI()` 创建应用，`@app.get("/health")` 注册健康检查路由。

**项目用途：** 后续用于承载 Chat、Provider、RAG、Agent 和 MCP 等后端 API。

## 38. Endpoint（接口端点）

**专业解释：** Endpoint 是由 HTTP Method 和 Path 共同确定的服务访问入口。

**大白话：** Method 表示要做什么，Path 表示要找哪个服务，两者组合才是一个完整接口。

**举例：** `GET /health` 是一个 Endpoint，`POST /health` 是另一个不同的 Endpoint。

**项目用途：** 用于组织服务健康检查、Chat 消息和模型配置等 API。

## 39. GET

**专业解释：** GET 是用于读取资源的 HTTP Method，通常不应修改服务器业务状态。

**大白话：** 它类似查询操作，只拿数据，不提交业务变更。

**举例：** `GET /health` 读取当前 API 服务状态。

**项目用途：** 后续用于读取会话、知识库列表和服务状态。

## 40. JSON

**专业解释：** JSON 是使用对象、数组和基础值表达结构化数据的文本格式。

**大白话：** 它和前端常见的 JavaScript Object 长得相似，是前后端传递数据的通用格式。

**举例：** FastAPI 会把 `ServiceStatus` 自动序列化为 JSON Response。

**项目用途：** Jack AI Studio 的大部分普通 HTTP API 都会使用 JSON 交换数据。

## 41. ASGI（异步服务器网关接口）

**专业解释：** ASGI 是 Python 异步 Web Server 与 Web Application 之间的标准接口。

**大白话：** 它像统一插座规范，让 Uvicorn 能启动并驱动 FastAPI 应用。

**举例：** Uvicorn 加载 `app.main:app`，通过 ASGI 把 HTTP Request 交给 FastAPI。

**项目用途：** 为未来流式响应、并发请求和长连接能力提供运行基础。

## 42. Uvicorn

**专业解释：** Uvicorn 是负责监听网络端口并运行 ASGI Application 的 Server。

**大白话：** FastAPI 定义“请求怎么处理”，Uvicorn 负责真正把服务开起来并接收请求。

**举例：** `uvicorn app.main:app --app-dir apps/api` 启动当前 API。

**项目用途：** 在本地开发和后续部署中运行 Jack AI Studio 的 FastAPI 应用。

## 43. Decorator（装饰器）

**专业解释：** Decorator 使用 `@` 语法包装或注册函数，在不修改函数主体调用方式的情况下附加行为。

**大白话：** 它像给函数贴一个标签，告诉 FastAPI 这个函数负责哪个 Method 和 Path。

**举例：** `@app.get("/health")` 把下方函数注册为健康检查处理函数。

**项目用途：** FastAPI 使用 Decorator 声明 API 路由、依赖和异常处理等行为。

## 44. Message（消息）

**专业解释：** Message 是模型对话中的结构化输入单元，通常包含发送者角色和文本内容。

**大白话：** 每句话不只记录“说了什么”，还要标明“是谁说的”。

**举例：** `{"role": "user", "content": "解释一下 Context Window"}` 表示一条用户消息。

**项目用途：** Jack AI Studio 会用 Message 组织 System 指令、用户输入和模型历史回答。

## 45. Message Role（消息角色）

**专业解释：** Message Role 表示消息在对话中的来源与语义职责，当前包括 `system`、`user` 和 `assistant`。

**大白话：** 它像聊天记录里的身份标签，让模型知道哪段是规则、哪段是提问、哪段是历史回答。

**举例：** `system` 规定回答方式，`user` 提问，`assistant` 保存模型上一轮回答。

**项目用途：** 用于构建有顺序、有身份的模型上下文。`system` 不是管理员权限，也不是可靠的安全边界。

## 46. Chat Request（对话请求）

**专业解释：** Chat Request 是一次模型推理所需输入的结构化集合，包含模型标识、消息列表和生成参数。

**大白话：** 它像提交给模型服务的一张完整订单，不能只写一句话，还要说明使用哪个模型和携带哪些历史消息。

**举例：** `ChatRequest` 当前包含 `provider`、`model`、`messages` 和 `temperature`。

**项目用途：** 它会成为后续 Chat Endpoint 与 Provider 调用之间的数据契约。

## 47. Temperature（温度）

**专业解释：** Temperature 是影响模型 Token 采样概率分布的生成参数，通常较低值更稳定，较高值更多样。

**大白话：** 它可以理解为回答时的“随机发挥程度”，但不是正确率或质量开关。

**举例：** 当前 `ChatRequest` 默认使用 `0.7`，并把允许范围约束为 `0～2`。

**项目用途：** 后续 Provider 会读取该参数控制生成风格，不同模型的实际支持范围仍需由适配层处理。

## 48. Provider Adapter（模型服务适配器）

**专业解释：** Provider Adapter 在项目数据契约与第三方模型 API 之间完成请求转换、调用和响应转换。

**大白话：** 它像统一请求层，让业务代码不用理解每家模型服务的参数细节。

**举例：** 把 `ChatRequest` 转成 OpenAI-compatible `messages`，再把返回文本转成 `ChatMessage`。

**项目用途：** 隔离第三方 SDK，为后续多 Provider 留出清晰边界。

## 49. SDK（软件开发工具包）

**专业解释：** SDK 是服务提供方封装的客户端库，负责认证、请求结构、网络调用和响应对象等能力。

**大白话：** 它类似项目使用 Axios，而不是每次手写底层 HTTP 连接。

**举例：** Python `openai` SDK 提供 `AsyncOpenAI` 客户端。

**项目用途：** Day 12 使用官方 SDK 建立异步 Provider 调用，不自行重复实现底层 HTTP。

## 50. Async I/O（异步输入输出）

**专业解释：** Async I/O 在等待网络或文件操作时释放执行权，使程序可以继续处理其他任务。

**大白话：** 它类似前端 `await fetch()` 或 Koa 的异步中间件，等待外部结果时不占着执行通道干等。

**举例：** `await client.chat.completions.create(...)` 等待模型服务响应。

**项目用途：** Provider 调用属于网络 I/O，异步方式有利于 FastAPI 后续并发处理多个 Chat 请求。

## 51. SecretStr（保密字符串）

**专业解释：** `SecretStr` 是 Pydantic 的敏感值类型，默认隐藏其字符串表示，降低日志意外泄漏风险。

**大白话：** 它像密码输入框的圆点遮罩，但仍需另外设置必填和长度校验。

**举例：** `ProviderConfig` 使用 `SecretStr` 保存 API Key，并使用 `min_length=1` 拒绝空值。

**项目用途：** 避免 Provider API Key 在配置对象的日志和调试输出中直接显示。

## 52. Mock（模拟对象）

**专业解释：** Mock 是测试中替代真实外部依赖的可控对象，用于观察调用参数并构造确定的返回结果。

**大白话：** 它像前端单测中替换 Axios；验证调用逻辑，但不会真的请求服务器。

**举例：** `FakeOpenAIClient` 记录模型、消息和 Temperature，并返回测试专用文本。

**项目用途：** 在不使用真实 API Key、不消耗额度的情况下测试 Provider Adapter。

## 53. Dependency Injection（依赖注入）

**专业解释：** Dependency Injection 从外部向函数或对象提供依赖，使调用方依赖清晰契约，而不是固定的创建过程。

**大白话：** 它类似 Vue 的 `provide/inject`；使用方说明需要什么，生产环境和测试环境可以提供不同实现。

**举例：** `POST /chat` 正常使用 `OpenAICompatibleProvider`，测试时通过 FastAPI Dependency Override 换成 `FakeChatProvider`。

**项目用途：** 隔离 Chat Route 与 Provider 创建过程，让 HTTP 链路能够在无真实 Key、无网络请求的条件下测试。

## 54. HTTP Error Mapping（HTTP 错误映射）

**专业解释：** HTTP Error Mapping 将应用内部异常转换为稳定的 HTTP Status Code 和对外错误响应。

**大白话：** 它像 Koa 的统一错误处理，把复杂内部错误翻译成前端能判断、又不会泄露内部细节的结果。

**举例：** `ChatRequest` 校验失败返回 `422`，Provider 无效响应返回 `502`，Provider 未配置返回 `503`。

**项目用途：** 为 Chat 客户端建立可预测的失败契约，并保护服务端配置和异常堆栈。

## 55. Backend for Frontend（BFF，服务于前端的后端层）

**专业解释：** BFF 是为特定前端提供的服务端接口层，用于适配前端访问方式、聚合请求或保护运行时配置，但不应复制核心业务逻辑。

**大白话：** 它像前端自己的服务台；浏览器只找同一个站点，服务台再联系真正处理业务的后端。

**举例：** 浏览器请求 Next.js `/api/chat`，Route Handler 使用服务端 `API_BASE_URL` 转发到 FastAPI `/chat`。

**项目用途：** 避免浏览器硬编码 FastAPI 地址和处理跨域，同时保证 Provider Key 只存在于 FastAPI 服务端。

## 56. Request State（请求状态）

**专业解释：** Request State 描述异步请求的 Idle、Loading、Success 和 Error 阶段，并驱动表单可用性、进度与结果展示。

**大白话：** 它就是用户点击发送后看到的“等待中、成功了、失败了”，不能让界面对请求状态毫无反馈。

**举例：** Chat 发送时禁用输入并显示等待提示，成功后展示 Assistant Message，失败后展示安全的中文错误。

**项目用途：** 让 Chat Workspace 能清楚表达模型请求是否正在处理以及最终结果。

## 57. Streaming（流式输出）

**专业解释：** Streaming 允许服务端在完整结果生成前持续发送已经得到的数据分片，客户端可以边接收边处理。

**大白话：** 它像做好一道菜就先上一道，不必等整桌全部完成。

**举例：** 模型生成一段文本，Chat 页面就立即追加一段，而不是等待完整回答。

**项目用途：** 降低 AI Chat 的首段等待时间，让用户看到回答正在生成。

## 58. Chunk（数据分片）

**专业解释：** Chunk 是流传输过程中一次读取到的数据片段，其边界不保证等于一个完整业务事件。

**大白话：** 一次到货可能只有半张单据，也可能同时装了两张单据，需要先拼接再拆分。

**举例：** `event: delta` 可能被两次 `reader.read()` 分开读到。

**项目用途：** Web SSE 解析器使用 Buffer 组合跨 Chunk 的完整 Event。

## 59. Server-Sent Events（SSE，服务器发送事件）

**专业解释：** SSE 是使用 `text/event-stream` 响应类型，在单个 HTTP Response 中持续传输文本事件的格式。

**大白话：** 它像服务端通过一条保持打开的 HTTP 水管，不断发送带标签的小纸条。

**举例：** 当前流使用 `delta` 传文本、`done` 表示完成、`error` 表示流内失败。

**项目用途：** 统一 FastAPI 到 Web 的 Streaming Chat 事件契约。

## 60. ReadableStream（可读流）

**专业解释：** ReadableStream 是 Web Streams API 的可读数据源，消费者可以使用 Reader 异步获取连续到达的字节分片。

**大白话：** 它像不断异步询问“下一段到了吗”，直到数据源结束。

**举例：** `response.body.getReader().read()` 逐段读取 FastAPI 透传回来的 SSE 文本。

**项目用途：** Web Chat 读取并解析 SSE，收到 `delta` 后立即更新 Assistant Message。

## 61. Async Generator（异步生成器）

**专业解释：** Async Generator 使用 `async def` 与 `yield` 定义，并通过 `async for` 逐项异步消费。

**大白话：** 它不是等全部完成后只返回一次，而是每拿到一段就交出去一段。

**举例：** Provider 的 `stream()` 每收到一个有效文本 Chunk 就 `yield content`。

**项目用途：** 串联 Provider AsyncStream、FastAPI StreamingResponse 和 SSE Event 生成过程。

## 62. Prompt Template（提示词模板）

**专业解释：** 带有固定指令结构和可替换变量的 Prompt，渲染后形成一次具体请求的文本。

**大白话：** 像一张可重复使用的表单，格式固定，主题等字段每次填写。

**举例：** `请解释 {{topic}}` 中的 `{{topic}}` 是模板变量。

**项目用途：** Day 17 用它组织概念讲解、方案对比和问题排查模板。

## 63. Variable Interpolation（变量插值）

**专业解释：** 将变量值填入模板占位符并生成完整文本的过程。

**大白话：** 把表单字段填入文档空格。

**举例：** `topic=Provider Registry` 会把 `{{topic}}` 替换为 `Provider Registry`。

**项目用途：** `renderPromptTemplate()` 负责纯文本渲染，组件负责收集变量值。

## 64. Prompt Catalog（提示词目录）

**专业解释：** 可供选择的 Prompt 模板及其元数据集合，不等于数据库持久化。

**大白话：** 像页面内置菜单，能选择菜品，但还没有保存成用户自己的菜单。

**举例：** `PROMPT_TEMPLATES` 保存模板 ID、标题、说明、正文和变量。

**项目用途：** Day 17 用本地 Catalog 验证模板复用流程，后续再接持久化。

## 65. Pure Function（纯函数）

**专业解释：** 对相同输入始终返回相同输出，并且不读取或修改外部状态的函数。

**大白话：** 像计算器，输入相同结果就相同，不会偷偷改页面或请求网络。

**举例：** `renderPromptTemplate(template, values)` 只返回渲染后的字符串。

**项目用途：** 将 Prompt 渲染逻辑从 React State 和 Chat 请求中隔离，便于测试和复用。

## 66. Structured Output（结构化输出）

**专业解释：** 要求模型按预先定义的数据结构返回结果，而不是只返回没有固定字段的自由文本。

**大白话：** 不只是让模型“回答问题”，还要求它按一张固定表格填写答案。

**举例：** Day 18 的回答必须包含 `summary`、`key_points`、`example` 和 `project_role`。

**项目用途：** `ChatRequest.output_mode=structured_answer` 让 Provider 请求 JSON Schema，API 再校验最终响应。

## 67. JSON Schema（JSON 数据结构约束）

**专业解释：** 描述 JSON 对象字段、类型、必填项和约束的机器可读规范。

**大白话：** 像给接口数据写的一份字段说明书，而且程序可以据此自动检查。

**举例：** `StructuredAnswer` 的 Schema 要求 `summary` 是非空字符串，`key_points` 是至少有一项的数组。

**项目用途：** Provider 使用它向模型声明输出格式，避免只依赖 Prompt 中的文字要求。

## 68. Response Validation（响应校验）

**专业解释：** 在收到外部服务响应后，根据运行时 Schema 验证内容是否满足业务契约。

**大白话：** 供应商说“我填好了”，后端还要逐项检查，不能只看 HTTP 200 就当作成功。

**举例：** `StructuredAnswer.model_validate_json(content)` 会拒绝缺少字段或 JSON 无效的 Provider 响应。

**项目用途：** 非流式和流式 Provider 结束后都必须通过结构校验；失败统一转为 `ProviderResponseError`。

## 69. Output Contract（输出契约）

**专业解释：** 调用方与模型服务共同遵守的输出格式约定，包含模式、字段和失败处理边界。

**大白话：** 前端、后端和模型都按同一张交付验收单工作。

**举例：** Web 发送 `structured_answer`，FastAPI 传递 JSON Schema，Provider 返回 JSON，API 验证四个字段后才认为成功。

**项目用途：** 把自由文本 Chat 与可消费的结构化数据区分开，为后续 Agent、Workflow 和 Tool 调用提供可靠输入。

## 70. Tool Calling（工具调用）

**专业解释：** 模型根据应用提供的工具定义，返回工具名、调用 ID 和参数的结构化请求；应用负责校验、授权和执行。

**大白话：** 模型只填写工具申请单，不会因为写了函数名就自动执行代码。

**举例：** 模型可以请求 `add_numbers` 并给出 `a=12`、`b=30`，API 必须先校验请求。

**项目用途：** Day 19 建立工具请求的数据边界，为后续 Provider 接入与安全执行做准备。

## 71. Tool Definition（工具定义）

**专业解释：** 描述工具类型、稳定名称、用途和参数 JSON Schema 的机器可读数据。

**大白话：** 它像 API 服务端交给模型的一份函数接口说明书。

**举例：** `add_numbers` 要求 `a`、`b` 都是必填整数，并禁止额外字段。

**项目用途：** 工具定义由 API 服务端构建，Web 不能随请求扩大可用工具范围。

## 72. Tool Call（工具调用请求）

**专业解释：** Provider 返回的结构化工具请求，包含 Tool Call ID、工具名和序列化参数。

**大白话：** 它是一张等待校验和执行的工单，不是工具结果。

**举例：** `RawToolCall(id="call_123", name="add_numbers", arguments="...")`。

**项目用途：** `validate_tool_call()` 把不可信 Raw Tool Call 转换为可信的 `ValidatedToolCall`。

## 73. Tool Arguments（工具参数）

**专业解释：** 模型为一次 Tool Call 生成的输入数据，在 Provider 边界通常以 JSON 字符串返回。

**大白话：** 模型填写了表单字段，但后端仍要检查字段、类型和数量。

**举例：** `{"a":12,"b":30}` 可通过，`{"a":"12","b":30}` 在严格模式下被拒绝。

**项目用途：** `AddNumbersArguments.model_validate_json()` 负责把原始字符串变成经过校验的 Python 对象。

## 74. Allowlist（允许列表）

**专业解释：** 只允许预先登记的标识继续处理，未登记值一律拒绝的安全策略。

**大白话：** 门卫只放名单上的工具进入，模型临时编出的危险函数名不能通过。

**举例：** `ChatToolName` 当前只允许 `add_numbers`，拒绝 `delete_project`。

**项目用途：** 防止 Provider Tool Call 越过服务端定义的工具能力边界。

## 75. ORM Model（对象关系映射模型）

**专业解释：** 使用代码声明数据库表、列、类型和约束，并在 Python 对象与关系型数据库记录之间建立映射的模型。

**大白话：** 它是“知道自己要落哪张表”的后端实体，不只是普通的数据字典。

**举例：** `User.email` 映射 `users.email`，并声明为非空且唯一。

**项目用途：** `apps/api/app/models/user.py` 为后续用户、会话和消息持久化提供数据库实体边界。

## 76. Declarative Base（声明式基类）

**专业解释：** SQLAlchemy ORM Model 共同继承的基类，集中持有已注册表结构的 `MetaData`。

**大白话：** 它像所有数据库表定义的总目录。

**举例：** `class User(Base)` 声明后，`Base.metadata` 可以发现 `users` 表。

**项目用途：** `apps/api/app/db/base.py` 提供未来 Migration 读取的统一元数据入口。

## 77. Repository（仓储层）

**专业解释：** 封装实体查询和写入操作的数据访问层，向业务 Service 提供稳定接口。

**大白话：** 业务代码说“按邮箱找用户”，不用自己拼每一条 SQLAlchemy 查询。

**举例：** `UserRepository.get_by_email()` 返回一个 `User` 或 `None`。

**项目用途：** 隔离 `User` 数据访问细节，并把事务提交留给未来 Service。

## 78. Flush（刷新事务变更）

**专业解释：** 将当前 Session 的待处理变更发送到数据库，使约束和生成值尽早生效，但不结束当前事务。

**大白话：** 先把修改送去处理，最终是否盖章还要等 `commit()`。

**举例：** `UserRepository.add()` 调用 `flush()`，但不调用 `commit()`。

**项目用途：** 保证未来一组用户、会话和消息操作可以由 Service 统一提交或回滚。
