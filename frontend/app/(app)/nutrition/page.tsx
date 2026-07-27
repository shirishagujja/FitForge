import { Plus } from "lucide-react";
import Link from "next/link";

import { WaterQuickAdd } from "@/components/nutrition/WaterQuickAdd";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";
import { todayIso } from "@/lib/date";

type Meal = {
  id: string;
  name: string;
  calories: number;
  logged_at: string;
};

type DailySummary = {
  total_calories: number;
  total_protein_g: number;
  total_carbs_g: number;
  total_fat_g: number;
  total_water_ml: number;
};

export default async function NutritionPage() {
  const today = todayIso();
  const [summaryRes, mealsRes] = await Promise.all([
    serverReadWithAccessToken(`/v1/nutrition/summary?date=${today}`),
    serverReadWithAccessToken(`/v1/meals?date_from=${today}&date_to=${today}`),
  ]);

  const summary: DailySummary = summaryRes.ok
    ? (await summaryRes.json()).data
    : {
        total_calories: 0,
        total_protein_g: 0,
        total_carbs_g: 0,
        total_fat_g: 0,
        total_water_ml: 0,
      };
  const meals: Meal[] = mealsRes.ok ? (await mealsRes.json()).data : [];

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight">Nutrition</h1>
        <Button asChild className="gap-2">
          <Link href="/nutrition/meals/new">
            <Plus className="h-4 w-4" />
            Log a meal
          </Link>
        </Button>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Calories
            </CardTitle>
          </CardHeader>
          <CardContent className="text-2xl font-bold">{summary.total_calories}</CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Protein</CardTitle>
          </CardHeader>
          <CardContent className="text-2xl font-bold">{summary.total_protein_g}g</CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Carbs</CardTitle>
          </CardHeader>
          <CardContent className="text-2xl font-bold">{summary.total_carbs_g}g</CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Water</CardTitle>
          </CardHeader>
          <CardContent className="text-2xl font-bold">{summary.total_water_ml}ml</CardContent>
        </Card>
      </div>

      <WaterQuickAdd today={today} />

      <div>
        <h2 className="mb-3 text-lg font-semibold">Today&apos;s meals</h2>
        {meals.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center gap-3 py-12 text-center">
              <p className="text-muted-foreground">No meals logged today.</p>
              <Button asChild variant="outline">
                <Link href="/nutrition/meals/new">Log your first meal</Link>
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="flex flex-col gap-3">
            {meals.map((meal) => (
              <Link key={meal.id} href={`/nutrition/meals/${meal.id}`}>
                <Card className="transition-colors hover:bg-accent">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0">
                    <CardTitle className="text-base">{meal.name}</CardTitle>
                    <span className="text-sm text-muted-foreground">{meal.calories} kcal</span>
                  </CardHeader>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
