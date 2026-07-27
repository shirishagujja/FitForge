import Link from "next/link";
import { notFound } from "next/navigation";

import { DeleteEntityButton } from "@/components/common/DeleteEntityButton";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";

type MealDetail = {
  id: string;
  name: string;
  logged_at: string;
  calories: number;
  protein_g: number | null;
  carbs_g: number | null;
  fat_g: number | null;
  notes: string | null;
};

export default async function MealDetailPage({
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
  const meal: MealDetail = body.data;

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">{meal.name}</h1>
          <p className="text-sm text-muted-foreground">
            {new Date(`${meal.logged_at}T00:00:00`).toLocaleDateString(undefined, {
              weekday: "long",
              month: "long",
              day: "numeric",
            })}
          </p>
        </div>
        <div className="flex gap-2">
          <Button asChild variant="outline">
            <Link href={`/nutrition/meals/${meal.id}/edit`}>Edit</Link>
          </Button>
          <DeleteEntityButton
            apiPath={`/api/meals/${meal.id}`}
            redirectTo="/nutrition"
            confirmMessage="Delete this meal? This cannot be undone."
            label="Delete meal"
          />
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">{meal.calories} kcal</CardTitle>
        </CardHeader>
        <CardContent className="flex gap-6 text-sm text-muted-foreground">
          {meal.protein_g != null && <span>{meal.protein_g}g protein</span>}
          {meal.carbs_g != null && <span>{meal.carbs_g}g carbs</span>}
          {meal.fat_g != null && <span>{meal.fat_g}g fat</span>}
        </CardContent>
        {meal.notes && (
          <CardContent className="pt-0 text-sm text-muted-foreground">{meal.notes}</CardContent>
        )}
      </Card>
    </div>
  );
}
