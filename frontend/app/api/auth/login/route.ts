import { NextResponse } from "next/server";

import { backendFetch } from "@/lib/auth/backend";
import { setAuthCookies } from "@/lib/auth/cookies";
import type { TokenResponseData } from "@/lib/auth/types";

export async function POST(request: Request) {
  const body = await request.text();
  const backendResponse = await backendFetch("/v1/auth/login", {
    method: "POST",
    body,
  });
  const payload = await backendResponse.json().catch(() => ({}));

  if (!backendResponse.ok) {
    return NextResponse.json(payload, { status: backendResponse.status });
  }

  const data = payload.data as TokenResponseData;
  const response = NextResponse.json({ data: { user: data.user } }, { status: 200 });
  setAuthCookies(response, {
    access_token: data.access_token,
    refresh_token: data.refresh_token,
    expires_in: data.expires_in,
  });
  return response;
}
