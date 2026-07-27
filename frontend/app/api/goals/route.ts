import { authedBackendFetch, toNextResponse } from "@/lib/auth/authedFetch";

export async function GET() {
  const result = await authedBackendFetch("/v1/goals");
  return toNextResponse(result);
}

export async function POST(request: Request) {
  const body = await request.text();
  const result = await authedBackendFetch("/v1/goals", { method: "POST", body });
  return toNextResponse(result);
}
