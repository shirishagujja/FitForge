"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/button";

type Goal = {
  id: string;
  title: string;
  target_weight_kg: number | null;
  target_date: string | null;
  status: "active" | "achieved" | "abandoned";
};

export function GoalActions({ goal }: { goal: Goal }) {
  const router = useRouter();
  const [isSaving, setIsSaving] = useState(false);

  async function markAchieved() {
    setIsSaving(true);
    await fetch(`/api/goals/${goal.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: goal.title,
        target_weight_kg: goal.target_weight_kg,
        target_date: goal.target_date,
        status: "achieved",
      }),
    });
    setIsSaving(false);
    router.refresh();
  }

  async function remove() {
    if (!confirm("Delete this goal?")) return;
    setIsSaving(true);
    await fetch(`/api/goals/${goal.id}`, { method: "DELETE" });
    setIsSaving(false);
    router.refresh();
  }

  return (
    <div className="flex gap-2">
      {goal.status === "active" && (
        <Button variant="outline" size="sm" disabled={isSaving} onClick={markAchieved}>
          Mark achieved
        </Button>
      )}
      <Button variant="ghost" size="sm" disabled={isSaving} onClick={remove}>
        Delete
      </Button>
    </div>
  );
}
