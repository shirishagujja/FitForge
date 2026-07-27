import { GoalForm } from "@/components/progress/GoalForm";

export default function NewGoalPage() {
  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold tracking-tight">Add a goal</h1>
      <GoalForm />
    </div>
  );
}
