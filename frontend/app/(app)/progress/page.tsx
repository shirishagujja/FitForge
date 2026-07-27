import { Plus } from "lucide-react";
import Link from "next/link";

import { GoalActions } from "@/components/progress/GoalActions";
import { WeightChart } from "@/components/progress/WeightChart";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";
import { todayIso } from "@/lib/date";

type Measurement = {
  id: string;
  recorded_at: string;
  weight_kg: number | null;
  body_fat_pct: number | null;
};

type Goal = {
  id: string;
  title: string;
  target_weight_kg: number | null;
  target_date: string | null;
  status: "active" | "achieved" | "abandoned";
};

export default async function ProgressPage() {
  const ninetyDaysAgo = new Date();
  ninetyDaysAgo.setDate(ninetyDaysAgo.getDate() - 90);
  const dateFrom = ninetyDaysAgo.toISOString().slice(0, 10);

  const [measurementsRes, goalsRes] = await Promise.all([
    serverReadWithAccessToken(`/v1/measurements?date_from=${dateFrom}&date_to=${todayIso()}`),
    serverReadWithAccessToken("/v1/goals"),
  ]);

  const measurements: Measurement[] = measurementsRes.ok
    ? (await measurementsRes.json()).data
    : [];
  const goals: Goal[] = goalsRes.ok ? (await goalsRes.json()).data : [];

  const chartData = measurements
    .filter((m) => m.weight_kg != null)
    .map((m) => ({ recorded_at: m.recorded_at, weight_kg: m.weight_kg as number }))
    .sort((a, b) => a.recorded_at.localeCompare(b.recorded_at));

  const latest = measurements[0];

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Progress</h1>
        <Button asChild className="gap-2">
          <Link href="/progress/measurements/new">
            <Plus className="h-4 w-4" />
            Log measurement
          </Link>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Weight trend</CardTitle>
        </CardHeader>
        <CardContent>
          {chartData.length === 0 ? (
            <div className="flex flex-col items-center gap-3 py-12 text-center">
              <p className="text-muted-foreground">No measurements logged yet.</p>
              <Button asChild variant="outline">
                <Link href="/progress/measurements/new">Log your first check-in</Link>
              </Button>
            </div>
          ) : (
            <>
              <WeightChart data={chartData} />
              {latest?.weight_kg != null && (
                <p className="mt-4 text-sm text-muted-foreground">
                  Latest: {latest.weight_kg}kg
                  {latest.body_fat_pct != null ? ` · ${latest.body_fat_pct}% body fat` : ""} on{" "}
                  {new Date(`${latest.recorded_at}T00:00:00`).toLocaleDateString(undefined, {
                    month: "short",
                    day: "numeric",
                  })}
                </p>
              )}
            </>
          )}
        </CardContent>
      </Card>

      <div>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold">Goals</h2>
          <Button asChild variant="outline" size="sm" className="gap-2">
            <Link href="/progress/goals/new">
              <Plus className="h-4 w-4" />
              Add goal
            </Link>
          </Button>
        </div>
        {goals.length === 0 ? (
          <Card>
            <CardContent className="py-8 text-center text-muted-foreground">
              No goals yet.
            </CardContent>
          </Card>
        ) : (
          <div className="flex flex-col gap-3">
            {goals.map((goal) => (
              <Card key={goal.id}>
                <CardHeader className="flex flex-row items-center justify-between space-y-0">
                  <div>
                    <div className="flex items-center gap-2">
                      <CardTitle className="text-base">{goal.title}</CardTitle>
                      {goal.status === "achieved" && <Badge>Achieved</Badge>}
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {goal.target_weight_kg ? `${goal.target_weight_kg}kg` : ""}
                      {goal.target_weight_kg && goal.target_date ? " · " : ""}
                      {goal.target_date
                        ? `by ${new Date(`${goal.target_date}T00:00:00`).toLocaleDateString(
                            undefined,
                            { month: "short", day: "numeric", year: "numeric" },
                          )}`
                        : ""}
                    </p>
                  </div>
                  <GoalActions goal={goal} />
                </CardHeader>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
