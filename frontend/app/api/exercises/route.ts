import { authedBackendFetch, toNextResponse } from "@/lib/auth/authedFetch";

export async function GET(request: Request) {
  const { search } = new URL(request.url);
  const result = await authedBackendFetch(`/v1/exercises${search}`);
  return toNextResponse(result);
}
