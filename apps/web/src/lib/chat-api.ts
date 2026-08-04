export type ChatMessageRole = "system" | "user" | "assistant";

export interface ChatMessage {
  role: ChatMessageRole;
  content: string;
}

export interface ChatRequest {
  model: string;
  messages: ChatMessage[];
  temperature: number;
}

export class ChatApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
    this.name = "ChatApiError";
  }
}

function isChatMessage(value: unknown): value is ChatMessage {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const message = value as Record<string, unknown>;

  return (
    (message.role === "system" ||
      message.role === "user" ||
      message.role === "assistant") &&
    typeof message.content === "string" &&
    message.content.length > 0
  );
}

function getErrorMessage(status: number): string {
  if (status === 422) {
    return "请求内容未通过 ChatRequest 校验，请检查 Model 和 Prompt。";
  }

  if (status === 502) {
    return "模型服务暂时没有返回有效回答，请稍后重试。";
  }

  if (status === 503) {
    return "AI Provider 尚未配置，请先在 FastAPI 服务端设置 API Key。";
  }

  return `Chat API 请求失败（HTTP ${status}）。`;
}

export async function createChatCompletion(
  request: ChatRequest,
): Promise<ChatMessage> {
  let response: Response;

  try {
    response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
  } catch {
    throw new ChatApiError("无法连接 Chat API，请确认 Web 服务正常。", 0);
  }

  if (!response.ok) {
    throw new ChatApiError(getErrorMessage(response.status), response.status);
  }

  const data: unknown = await response.json();

  if (!isChatMessage(data) || data.role !== "assistant") {
    throw new ChatApiError("Chat API 响应不符合 Assistant Message 契约。", 502);
  }

  return data;
}
