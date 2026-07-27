"use client";

import { useRouter } from "next/navigation";
import { useState, type FormEvent } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

type GeneratedMeal = {
  name: string;
  estimated_calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
};

export default function AiMealsPage() {
  const router = useRouter();
  const [mealType, setMealType] = useState("lunch");
  const [restrictions, setRestrictions] = useState("");
  const [targetCalories, setTargetCalories] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [loggingIndex, setLoggingIndex] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<GeneratedMeal[]>([]);

  async function onGenerate(event: FormEvent) {
    event.preventDefault();
    setError(null);
    setSuggestions([]);
    setIsGenerating(true);
    try {
      const response = await fetch("/api/ai/generate-meals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          meal_type: mealType,
          dietary_restrictions: restrictions || null,
          target_calories: targetCalories ? Number(targetCalories) : null,
        }),
      });
      const body = await response.json();
      if (!response.ok) {
        setError(body?.error?.message ?? "Couldn't generate meal ideas. Please try again.");
        return;
      }
      setSuggestions(body.data.suggestions);
    } finally {
      setIsGenerating(false);
    }
  }

  async function onLog(meal: GeneratedMeal, index: number) {
    setLoggingIndex(index);
    setError(null);
    try {
      const response = await fetch("/api/meals", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: meal.name,
          logged_at: new Date().toISOString().slice(0, 10),
          calories: meal.estimated_calories,
          protein_g: meal.protein_g,
          carbs_g: meal.carbs_g,
          fat_g: meal.fat_g,
          notes: "Suggested by AI Coach",
        }),
      });
      const body = await response.json();
      if (!response.ok) {
        setError(body?.error?.message ?? "Couldn't log this meal. Please try again.");
        return;
      }
      router.push(`/nutrition/meals/${body.data.id}`);
    } finally {
      setLoggingIndex(null);
    }
  }

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <h1 className="text-2xl font-bold tracking-tight">Get meal ideas</h1>

      <Card>
        <CardContent className="pt-6">
          <form onSubmit={onGenerate} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="mealType">Meal type</Label>
              <Input
                id="mealType"
                placeholder="breakfast, lunch, dinner, snack…"
                value={mealType}
                onChange={(e) => setMealType(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="restrictions">Dietary restrictions (optional)</Label>
              <Input
                id="restrictions"
                placeholder="Vegetarian, gluten-free…"
                value={restrictions}
                onChange={(e) => setRestrictions(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="targetCalories">Target calories (optional)</Label>
              <Input
                id="targetCalories"
                type="number"
                min={0}
                max={3000}
                value={targetCalories}
                onChange={(e) => setTargetCalories(e.target.value)}
              />
            </div>
            {error && <p className="text-sm font-medium text-destructive">{error}</p>}
            <Button type="submit" disabled={isGenerating}>
              {isGenerating ? "Generating…" : "Get suggestions"}
            </Button>
          </form>
        </CardContent>
      </Card>

      {suggestions.length > 0 && (
        <div className="flex flex-col gap-3">
          {suggestions.map((meal, index) => (
            <Card key={index}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0">
                <div>
                  <CardTitle className="text-base">{meal.name}</CardTitle>
                  <p className="text-sm text-muted-foreground">
                    {meal.estimated_calories} kcal · {meal.protein_g}g protein ·{" "}
                    {meal.carbs_g}g carbs · {meal.fat_g}g fat
                  </p>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={loggingIndex === index}
                  onClick={() => onLog(meal, index)}
                >
                  {loggingIndex === index ? "Logging…" : "Log this meal"}
                </Button>
              </CardHeader>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
