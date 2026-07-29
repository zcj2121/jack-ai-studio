export interface ServiceStatus {
  name: string;
  status: string;
  python_version: string;
  planned_capabilities: string[];
}

export type ApiHealth =
  | {
      state: "online";
      data: ServiceStatus;
    }
  | {
      state: "offline";
      message: string;
    };

const DEFAULT_API_BASE_URL = "http://127.0.0.1:8000";

function isServiceStatus(value: unknown): value is ServiceStatus {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const status = value as Record<string, unknown>;

  return (
    typeof status.name === "string" &&
    typeof status.status === "string" &&
    typeof status.python_version === "string" &&
    Array.isArray(status.planned_capabilities) &&
    status.planned_capabilities.every(
      (capability) => typeof capability === "string",
    )
  );
}

export async function getApiHealth(): Promise<ApiHealth> {
  const apiBaseUrl = process.env.API_BASE_URL ?? DEFAULT_API_BASE_URL;

  try {
    const response = await fetch(`${apiBaseUrl}/health`, {
      cache: "no-store",
      signal: AbortSignal.timeout(2_000),
    });

    if (!response.ok) {
      return {
        state: "offline",
        message: `API 返回 HTTP ${response.status}`,
      };
    }

    const data: unknown = await response.json();

    if (!isServiceStatus(data)) {
      return {
        state: "offline",
        message: "API 响应结构不符合 ServiceStatus",
      };
    }

    return {
      state: "online",
      data,
    };
  } catch {
    return {
      state: "offline",
      message: "无法连接 FastAPI，请确认服务已启动",
    };
  }
}
