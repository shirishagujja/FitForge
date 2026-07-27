import { authedBackendFetch, toNextResponse } from "@/lib/auth/authedFetch";

export async function GET(request: Request) {
  const { search } = new URL(request.url);
  const result = await authedBackendFetch(`/v1/measurements${search}`);
  return toNextResponse(result);
}

export async function POST(request: Request) {
  const body = await request.text();
  const result = await authedBackendFetch("/v1/measurements", { method: "POST", body });
  return toNextResponse(result);
}
