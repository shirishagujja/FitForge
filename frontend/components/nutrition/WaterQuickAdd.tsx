"use client";

import { Droplet } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function WaterQuickAdd({ today }: { today: string }) {
  const router = useRouter();
  const [isSaving, setIsSaving] = useState(false);

  async function addWater(amountMl: number) {
    setIsSaving(true);
    await fetch("/api/water-entries", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ logged_at: today, amount_ml: amountMl }),
    });
    setIsSaving(false);
    router.refresh();
  }

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
          <Droplet className="h-4 w-4" />
          Add water
        </CardTitle>
      </CardHeader>
      <CardContent className="flex gap-2">
        <Button variant="outline" size="sm" disabled={isSaving} onClick={() => addWater(250)}>
          +250ml
        </Button>
        <Button variant="outline" size="sm" disabled={isSaving} onClick={() => addWater(500)}>
          +500ml
        </Button>
      </CardContent>
    </Card>
  );
}
