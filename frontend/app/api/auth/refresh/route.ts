import { NextResponse } from "next/server";

import { clearAuthCookies, setAuthCookies } from "@/lib/auth/cookies";
import { performRefresh } from "@/lib/auth/refresh";

export async function POST() {
  const result = await performRefresh();

  if (!result.ok) {
    const response = NextResponse.json(
      {
        error: {
          code: "UNAUTHORIZED",
          message: "Session expired",
          details: [],
          correlation_id: "",
        },
      },
      { status: 401 },
    );
    clearAuthCookies(response);
    return response;
  }

  const response = NextResponse.json({ data: { user: result.user } }, { status: 200 });
  setAuthCookies(response, result.tokens);
  return response;
}
