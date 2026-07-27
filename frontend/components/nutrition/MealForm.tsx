"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useForm } from "react-hook-form";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { mealSchema, type MealFormInput, type MealFormValues } from "@/lib/validation/nutrition";

export function MealForm({
  mealId,
  defaultValues,
}: {
  mealId?: string;
  defaultValues?: MealFormValues;
}) {
  const router = useRouter();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<MealFormInput, unknown, MealFormValues>({
    resolver: zodResolver(mealSchema),
    defaultValues: defaultValues ?? {
      name: "",
      logged_at: new Date().toISOString().slice(0, 10),
      calories: 0,
      protein_g: "",
      carbs_g: "",
      fat_g: "",
      notes: "",
    },
  });

  async function onSubmit(values: MealFormValues) {
    setServerError(null);
    const payload = {
      name: values.name,
      logged_at: values.logged_at,
      calories: values.calories,
      protein_g: values.protein_g ? Number(values.protein_g) : null,
      carbs_g: values.carbs_g ? Number(values.carbs_g) : null,
      fat_g: values.fat_g ? Number(values.fat_g) : null,
      notes: values.notes || null,
    };

    const url = mealId ? `/api/meals/${mealId}` : "/api/meals";
    const method = mealId ? "PUT" : "POST";
    const response = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const body = await response.json();

    if (!response.ok) {
      setServerError(body?.error?.message ?? "Something went wrong. Please try again.");
      return;
    }

    router.push(`/nutrition/meals/${body.data.id}`);
    router.refresh();
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Meal details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input placeholder="Grilled chicken salad" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="logged_at"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Date</FormLabel>
                  <FormControl>
                    <Input type="date" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="calories"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Calories</FormLabel>
                  <FormControl>
                    <Input
                      type="number"
                      min={0}
                      {...field}
                      value={(field.value as number | string | undefined) ?? ""}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="grid grid-cols-3 gap-3">
              <FormField
                control={form.control}
                name="protein_g"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Protein (g)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} step="0.5" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="carbs_g"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Carbs (g)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} step="0.5" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="fat_g"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Fat (g)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} step="0.5" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>
            <FormField
              control={form.control}
              name="notes"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Notes (optional)</FormLabel>
                  <FormControl>
                    <Input placeholder="Any details?" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </CardContent>
        </Card>

        {serverError && <p className="text-sm font-medium text-destructive">{serverError}</p>}

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? "Saving…" : mealId ? "Save changes" : "Log meal"}
        </Button>
      </form>
    </Form>
  );
}
