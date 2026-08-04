const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";
const CHAT_TIMEOUT_MS = 60_000;

export async function POST(request: Request) {
  const apiBaseUrl = (
    process.env.API_BASE_URL ?? DEFAULT_API_BASE_URL
  ).replace(/\/$/, "");

  try {
    const response = await fetch(`${apiBaseUrl}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: await request.text(),
      cache: "no-store",
      signal: AbortSignal.timeout(CHAT_TIMEOUT_MS),
    });
    const body = await response.text();

    return new Response(body, {
      status: response.status,
      headers: {
        "Content-Type":
          response.headers.get("Content-Type") ?? "application/json",
      },
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
