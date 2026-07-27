import Link from "next/link";
import { notFound } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DeleteEntityButton } from "@/components/common/DeleteEntityButton";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";

type WorkoutDetail = {
  id: string;
  name: string;
  performed_at: string;
  notes: string | null;
  exercises: {
    id: string;
    exercise: { name: string };
    sets: number;
    reps: number;
    weight_kg: number | null;
    notes: string | null;
  }[];
};

export default async function WorkoutDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const response = await serverReadWithAccessToken(`/v1/workouts/${id}`);
  if (response.status === 404) {
    notFound();
  }
  const body = await response.json();
  const workout: WorkoutDetail = body.data;

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{workout.name}</h1>
          <p className="text-sm text-muted-foreground">
            {new Date(`${workout.performed_at}T00:00:00`).toLocaleDateString(undefined, {
              weekday: "long",
              month: "long",
              day: "numeric",
            })}
          </p>
        </div>
        <div className="flex gap-2">
          <Button asChild variant="outline">
            <Link href={`/workouts/${workout.id}/edit`}>Edit</Link>
          </Button>
          <DeleteEntityButton
            apiPath={`/api/workouts/${workout.id}`}
            redirectTo="/workouts"
            confirmMessage="Delete this workout? This cannot be undone."
            label="Delete workout"
          />
        </div>
      </div>

      {workout.notes && <p className="text-sm text-muted-foreground">{workout.notes}</p>}

      <div className="flex flex-col gap-3">
        {workout.exercises.map((we) => (
          <Card key={we.id}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0">
              <CardTitle className="text-base">{we.exercise.name}</CardTitle>
              <span className="text-sm text-muted-foreground">
                {we.sets} x {we.reps}
                {we.weight_kg ? ` @ ${we.weight_kg}kg` : ""}
              </span>
            </CardHeader>
            {we.notes && (
              <CardContent className="pt-0 text-sm text-muted-foreground">
                {we.notes}
              </CardContent>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
}
