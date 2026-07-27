import { notFound } from "next/navigation";

import { MealForm } from "@/components/nutrition/MealForm";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";
import type { MealFormValues } from "@/lib/validation/nutrition";

export default async function EditMealPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const response = await serverReadWithAccessToken(`/v1/meals/${id}`);
  if (response.status === 404) {
    notFound();
  }
  const body = await response.json();
  const meal = body.data;

  const defaultValues: MealFormValues = {
    name: meal.name,
    logged_at: meal.logged_at,
    calories: meal.calories,
    protein_g: meal.protein_g?.toString() ?? "",
    carbs_g: meal.carbs_g?.toString() ?? "",
    fat_g: meal.fat_g?.toString() ?? "",
    notes: meal.notes ?? "",
  };

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold tracking-tight">Edit meal</h1>
      <MealForm mealId={id} defaultValues={defaultValues} />
    </div>
  );
}
