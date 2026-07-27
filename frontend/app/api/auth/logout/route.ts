import { cookies } from "next/headers";
import { NextResponse } from "next/server";

import { backendFetch } from "@/lib/auth/backend";
import { clearAuthCookies, REFRESH_COOKIE } from "@/lib/auth/cookies";

export async function POST() {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get(REFRESH_COOKIE)?.value;

  if (refreshToken) {
    await backendFetch("/v1/auth/logout", {
      method: "POST",
      body: JSON.stringify({ refresh_token: refreshToken }),
    }).catch(() => undefined);
  }

  const response = NextResponse.json({ data: null, message: "Logged out successfully" });
  clearAuthCookies(response);
  return response;
}
