import { cookies } from "next/headers";

import { backendFetch } from "@/lib/auth/backend";
import { REFRESH_COOKIE, type TokenPair } from "@/lib/auth/cookies";
import type { AuthUser, TokenResponseData } from "@/lib/auth/types";

export type RefreshResult = { ok: true; tokens: TokenPair; user: AuthUser } | { ok: false };

/** Rotates the refresh token cookie into a fresh access+refresh pair. Does not set cookies itself. */
export async function performRefresh(): Promise<RefreshResult> {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get(REFRESH_COOKIE)?.value;
  if (!refreshToken) return { ok: false };

  const backendResponse = await backendFetch("/v1/auth/refresh", {
    method: "POST",
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!backendResponse.ok) return { ok: false };

  const payload = (await backendResponse.json().catch(() => undefined)) as
    | { data: TokenResponseData }
    | undefined;
  const data = payload?.data;
  if (!data?.access_token || !data?.refresh_token) return { ok: false };

  return {
    ok: true,
    tokens: {
      access_token: data.access_token,
      refresh_token: data.refresh_token,
      expires_in: data.expires_in,
    },
    user: data.user,
  };
}
