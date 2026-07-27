import { authedBackendFetch, toNextResponse } from "@/lib/auth/authedFetch";

export async function GET() {
  const result = await authedBackendFetch("/v1/ai/recommendations");
  return toNextResponse(result);
}
