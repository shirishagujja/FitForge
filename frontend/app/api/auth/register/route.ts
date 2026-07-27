import { NextResponse } from "next/server";

import { backendFetch } from "@/lib/auth/backend";

export async function POST(request: Request) {
  const body = await request.text();
  const backendResponse = await backendFetch("/v1/auth/register", {
    method: "POST",
    body,
  });
  const payload = await backendResponse.json().catch(() => ({}));
  return NextResponse.json(payload, { status: backendResponse.status });
}
