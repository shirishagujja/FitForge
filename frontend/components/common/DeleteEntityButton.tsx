"use client";

import { Trash2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/button";

export function DeleteEntityButton({
  apiPath,
  redirectTo,
  confirmMessage = "Delete this? This cannot be undone.",
  label = "Delete",
}: {
  apiPath: string;
  redirectTo: string;
  confirmMessage?: string;
  label?: string;
}) {
  const router = useRouter();
  const [isDeleting, setIsDeleting] = useState(false);

  async function onDelete() {
    if (!confirm(confirmMessage)) return;
    setIsDeleting(true);
    await fetch(apiPath, { method: "DELETE" });
    router.push(redirectTo);
    router.refresh();
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      aria-label={label}
      onClick={onDelete}
      disabled={isDeleting}
    >
      <Trash2 className="h-4 w-4" />
    </Button>
  );
}
