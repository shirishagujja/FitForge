import { MealForm } from "@/components/nutrition/MealForm";

export default function NewMealPage() {
  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold tracking-tight">Log a meal</h1>
      <MealForm />
    </div>
  );
}
