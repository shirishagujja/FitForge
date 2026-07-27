import { authedBackendFetch, toNextResponse } from "@/lib/auth/authedFetch";

export async function POST(request: Request) {
  const body = await request.text();
  const result = await authedBackendFetch("/v1/ai/generate-workout", { method: "POST", body });
  return toNextResponse(result);
}
