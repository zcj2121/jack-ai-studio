const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";
const CHAT_TIMEOUT_MS = 60_000;

type ChatEndpointPath = "/chat" | "/chat/stream";

export async function forwardChatRequest(
  request: Request,
  endpointPath: ChatEndpointPath,
): Promise<Response> {
  const apiBaseUrl = (
    process.env.API_BASE_URL ?? DEFAULT_API_BASE_URL
  ).replace(/\/$/, "");

  try {
    const response = await fetch(`${apiBaseUrl}${endpointPath}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: await request.text(),
      cache: "no-store",
      signal: AbortSignal.any([
        request.signal,
        AbortSignal.timeout(CHAT_TIMEOUT_MS),
      ]),
    });
    const headers = new Headers();

    for (const headerName of [
      "Content-Type",
      "Cache-Control",
      "X-Accel-Buffering",
    ]) {
      const headerValue = response.headers.get(headerName);

      if (headerValue !== null) {
        headers.set(headerName, headerValue);
      }
    }

    return new Response(response.body, {
      status: response.status,
      headers,
    });
  } catch {
    return Response.json(
      {
        detail: "Unable to connect to Jack AI Studio API",
      },
      {
        status: 502,
      },
    );
  }
}
