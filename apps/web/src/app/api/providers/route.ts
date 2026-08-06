import { forwardProviderCatalogRequest } from "@/lib/server/chat-proxy";

export async function GET(request: Request) {
  return forwardProviderCatalogRequest(request);
}
