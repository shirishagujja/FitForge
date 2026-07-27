import { authedBackendFetch, toNextResponse } from "@/lib/auth/authedFetch";

export async function PUT(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const body = await request.text();
  const result = await authedBackendFetch(`/v1/goals/${id}`, { method: "PUT", body });
  return toNextResponse(result);
}

export async function DELETE(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const result = await authedBackendFetch(`/v1/goals/${id}`, { method: "DELETE" });
  return toNextResponse(result);
}
