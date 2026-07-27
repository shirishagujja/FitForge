import { Plus } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";

type WorkoutSummary = {
  id: string;
  name: string;
  performed_at: string;
  exercise_count: number;
};

export default async function WorkoutsPage() {
  const response = await serverReadWithAccessToken("/v1/workouts");
  const body = await response.json();
  const workouts: WorkoutSummary[] = response.ok ? body.data : [];

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Workouts</h1>
        <Button asChild className="gap-2">
          <Link href="/workouts/new">
            <Plus className="h-4 w-4" />
            New workout
          </Link>
        </Button>
      </div>

      {workouts.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-3 py-12 text-center">
            <p className="text-muted-foreground">You haven&apos;t logged a workout yet.</p>
            <Button asChild variant="outline">
              <Link href="/workouts/new">Log your first workout</Link>
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="flex flex-col gap-3">
          {workouts.map((workout) => (
            <Link key={workout.id} href={`/workouts/${workout.id}`}>
              <Card className="transition-colors hover:bg-accent">
                <CardHeader className="flex flex-row items-center justify-between space-y-0">
                  <div>
                    <CardTitle className="text-base">{workout.name}</CardTitle>
                    <p className="text-sm text-muted-foreground">
                      {new Date(`${workout.performed_at}T00:00:00`).toLocaleDateString(undefined, {
                        weekday: "short",
                        month: "short",
                        day: "numeric",
                      })}
                    </p>
                  </div>
                  <span className="text-sm text-muted-foreground">
                    {workout.exercise_count} exercise{workout.exercise_count === 1 ? "" : "s"}
                  </span>
                </CardHeader>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
