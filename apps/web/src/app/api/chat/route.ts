import { forwardChatRequest } from "@/lib/server/chat-proxy";

export async function POST(request: Request) {
  return forwardChatRequest(request, "/chat");
}
