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

interface ChatStreamDelta {
  content: string;
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

async function postChatRequest(
  endpoint: "/api/chat" | "/api/chat/stream",
  request: ChatRequest,
): Promise<Response> {
  try {
    return await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
  } catch {
    throw new ChatApiError("无法连接 Chat API，请确认 Web 服务正常。", 0);
  }
}

function parseStreamDelta(data: string): ChatStreamDelta {
  let payload: unknown;

  try {
    payload = JSON.parse(data);
  } catch {
    throw new ChatApiError("Chat Stream 返回了无效 JSON。", 502);
  }

  if (typeof payload !== "object" || payload === null) {
    throw new ChatApiError("Chat Stream 事件结构无效。", 502);
  }

  const delta = payload as Record<string, unknown>;

  if (typeof delta.content !== "string" || delta.content.length === 0) {
    throw new ChatApiError("Chat Stream 缺少文本分片。", 502);
  }

  return {
    content: delta.content,
  };
}

function handleSseFrame(
  frame: string,
  onDelta: (content: string) => void,
): boolean {
  let eventName = "message";
  const dataLines: string[] = [];

  for (const line of frame.split("\n")) {
    if (line.startsWith("event:")) {
      eventName = line.slice("event:".length).trim();
    } else if (line.startsWith("data:")) {
      dataLines.push(line.slice("data:".length).trimStart());
    }
  }

  const data = dataLines.join("\n");

  if (eventName === "delta") {
    onDelta(parseStreamDelta(data).content);
    return false;
  }

  if (eventName === "error") {
    throw new ChatApiError(
      "模型流式响应中断，请稍后重试。",
      502,
    );
  }

  return eventName === "done";
}

export async function createChatCompletion(
  request: ChatRequest,
): Promise<ChatMessage> {
  const response = await postChatRequest("/api/chat", request);

  if (!response.ok) {
    throw new ChatApiError(getErrorMessage(response.status), response.status);
  }

  const data: unknown = await response.json();

  if (!isChatMessage(data) || data.role !== "assistant") {
    throw new ChatApiError("Chat API 响应不符合 Assistant Message 契约。", 502);
  }

  return data;
}

export async function streamChatCompletion(
  request: ChatRequest,
  onDelta: (content: string) => void,
): Promise<void> {
  const response = await postChatRequest("/api/chat/stream", request);

  if (!response.ok) {
    throw new ChatApiError(getErrorMessage(response.status), response.status);
  }

  if (response.body === null) {
    throw new ChatApiError("Chat API 没有返回可读取的 Stream。", 502);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();

    if (done) {
      buffer += decoder.decode();
      break;
    }

    buffer += decoder.decode(value, { stream: true });
    buffer = buffer.replaceAll("\r\n", "\n");

    let boundaryIndex = buffer.indexOf("\n\n");

    while (boundaryIndex >= 0) {
      const frame = buffer.slice(0, boundaryIndex).trim();
      buffer = buffer.slice(boundaryIndex + 2);

      if (frame && handleSseFrame(frame, onDelta)) {
        await reader.cancel();
        return;
      }

      boundaryIndex = buffer.indexOf("\n\n");
    }
  }

  const finalFrame = buffer.trim();

  if (finalFrame && handleSseFrame(finalFrame, onDelta)) {
    return;
  }

  throw new ChatApiError("Chat Stream 在完成事件前意外结束。", 502);
}
