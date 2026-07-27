import { authedBackendFetch, toNextResponse } from "@/lib/auth/authedFetch";

export async function DELETE(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const result = await authedBackendFetch(`/v1/water-entries/${id}`, { method: "DELETE" });
  return toNextResponse(result);
}
