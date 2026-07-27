import { notFound } from "next/navigation";

import { WorkoutForm, type ExerciseOption } from "@/components/workouts/WorkoutForm";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";
import type { WorkoutFormValues } from "@/lib/validation/workouts";

type WorkoutExerciseDetail = {
  exercise: { id: string };
  sets: number;
  reps: number;
  weight_kg: number | null;
  notes: string | null;
};

export default async function EditWorkoutPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const [exercisesRes, workoutRes] = await Promise.all([
    serverReadWithAccessToken("/v1/exercises"),
    serverReadWithAccessToken(`/v1/workouts/${id}`),
  ]);

  if (workoutRes.status === 404) {
    notFound();
  }

  const exercisesBody = await exercisesRes.json();
  const workoutBody = await workoutRes.json();

  const exercises: ExerciseOption[] = exercisesRes.ok ? exercisesBody.data : [];
  const workout = workoutBody.data;

  const defaultValues: WorkoutFormValues = {
    name: workout.name,
    performed_at: workout.performed_at,
    notes: workout.notes ?? "",
    exercises: workout.exercises.map((we: WorkoutExerciseDetail) => ({
      exercise_id: we.exercise.id,
      sets: we.sets,
      reps: we.reps,
      weight_kg: we.weight_kg?.toString() ?? "",
      notes: we.notes ?? "",
    })),
  };

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold tracking-tight">Edit workout</h1>
      <WorkoutForm exercises={exercises} workoutId={id} defaultValues={defaultValues} />
    </div>
  );
}
