const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost/api";

export type ApiEnvelope<T> = {
  data: T;
};

export type ApiErrorEnvelope = {
  error: {
    code: string;
    message: string;
    details: unknown[];
    correlation_id: string;
  };
};

export class ApiClientError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly body?: ApiErrorEnvelope,
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL.replace(/\/$/, "")}${path.startsWith("/") ? path : `/${path}`}`;

  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    let body: ApiErrorEnvelope | undefined;
    try {
      body = (await response.json()) as ApiErrorEnvelope;
    } catch {
      // Response may not be JSON
    }
    throw new ApiClientError(
      body?.error?.message ?? `Request failed with status ${response.status}`,
      response.status,
      body,
    );
  }

  return (await response.json()) as T;
}

export const apiClient = {
  getHealth: () => request<ApiEnvelope<{ status: string }>>("/v1/health"),
  getReady: () =>
    request<ApiEnvelope<{ status: string; checks: Record<string, string> }>>("/v1/ready"),
  verifyEmail: (token: string) =>
    request<{ data: { email_verified: boolean }; message: string }>(
      `/v1/auth/verify-email?token=${encodeURIComponent(token)}`,
    ),
  resetPassword: (payload: {
    token: string;
    password: string;
    password_confirm: string;
  }) =>
    request<{ data: null; message: string }>("/v1/auth/reset-password", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  forgotPassword: (email: string) =>
    request<{ data: null; message: string }>("/v1/auth/forgot-password", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),
};

export { API_BASE_URL };
