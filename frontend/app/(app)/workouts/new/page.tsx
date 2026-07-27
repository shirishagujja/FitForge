import { WorkoutForm, type ExerciseOption } from "@/components/workouts/WorkoutForm";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";

export default async function NewWorkoutPage() {
  const response = await serverReadWithAccessToken("/v1/exercises");
  const body = await response.json();
  const exercises: ExerciseOption[] = response.ok ? body.data : [];

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold tracking-tight">New workout</h1>
      <WorkoutForm exercises={exercises} />
    </div>
  );
}
