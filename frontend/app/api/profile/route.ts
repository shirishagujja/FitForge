import { authedBackendFetch, toNextResponse } from "@/lib/auth/authedFetch";

export async function GET() {
  const result = await authedBackendFetch("/v1/profile");
  return toNextResponse(result);
}

export async function PUT(request: Request) {
  const body = await request.text();
  const result = await authedBackendFetch("/v1/profile", { method: "PUT", body });
  return toNextResponse(result);
}
