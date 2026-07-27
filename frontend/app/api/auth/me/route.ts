import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { backendFetch } from "@/lib/auth/backend";
import { ACCESS_COOKIE, clearAuthCookies, setAuthCookies } from "@/lib/auth/cookies";
import { performRefresh } from "@/lib/auth/refresh";

async function fetchMe(accessToken: string) {
  return backendFetch("/v1/auth/me", {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

export async function GET() {
  const cookieStore = await cookies();
  const accessToken = cookieStore.get(ACCESS_COOKIE)?.value;

  if (accessToken) {
    const backendResponse = await fetchMe(accessToken);
    if (backendResponse.ok) {
      const payload = await backendResponse.json();
      return NextResponse.json(payload, { status: 200 });
    }
  }

  // Access token missing or expired — try a single silent refresh before giving up.
  const refreshResult = await performRefresh();
  if (!refreshResult.ok) {
    const response = NextResponse.json(
      {
        error: {
          code: "UNAUTHORIZED",
          message: "Not authenticated",
          details: [],
          correlation_id: "",
        },
      },
      { status: 401 },
    );
    clearAuthCookies(response);
    return response;
  }

  const meResponse = await fetchMe(refreshResult.tokens.access_token);
  const meBody = meResponse.ok
    ? await meResponse.json()
    : { data: refreshResult.user };

  const response = NextResponse.json(meBody, { status: 200 });
  setAuthCookies(response, refreshResult.tokens);
  return response;
}
