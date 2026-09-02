import type { ChatRequest } from "@/lib/chat-api";

const DEMO_CHUNKS = [
  "## Provider 流式回答\n\n",
  "这是一个不需要 API Key 的本地演示。\n\n",
  "- Provider 负责调用模型服务\n- 流式传输负责逐段返回文本\n- Markdown 负责展示层排版\n\n",
  "```ts\nconst answer = await streamChatCompletion(request)\n```\n",
];

const DEMO_CHUNK_DELAY_MS = 420;

export async function streamMarkdownDemo(
  _request: ChatRequest,
  onDelta: (content: string) => void,
): Promise<void> {
  for (const chunk of DEMO_CHUNKS) {
    await new Promise((resolve) => {
      window.setTimeout(resolve, DEMO_CHUNK_DELAY_MS);
    });
    onDelta(chunk);
  }
}
