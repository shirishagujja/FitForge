"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { Plus, Trash2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useFieldArray, useForm } from "react-hook-form";

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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  workoutSchema,
  type WorkoutFormInput,
  type WorkoutFormValues,
} from "@/lib/validation/workouts";

export type ExerciseOption = { id: string; name: string; category: string };

export function WorkoutForm({
  exercises,
  workoutId,
  defaultValues,
}: {
  exercises: ExerciseOption[];
  workoutId?: string;
  defaultValues?: WorkoutFormValues;
}) {
  const router = useRouter();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<WorkoutFormInput, unknown, WorkoutFormValues>({
    resolver: zodResolver(workoutSchema),
    defaultValues: defaultValues ?? {
      name: "",
      performed_at: new Date().toISOString().slice(0, 10),
      notes: "",
      exercises: [],
    },
  });

  const { fields, append, remove } = useFieldArray({ control: form.control, name: "exercises" });
  const exercisesError = form.formState.errors.exercises;
  const exercisesErrorMessage =
    exercisesError && "message" in exercisesError ? (exercisesError.message as string) : undefined;

  async function onSubmit(values: WorkoutFormValues) {
    setServerError(null);
    const payload = {
      name: values.name,
      performed_at: values.performed_at,
      notes: values.notes || null,
      exercises: values.exercises.map((e) => ({
        exercise_id: e.exercise_id,
        sets: e.sets,
        reps: e.reps,
        weight_kg: e.weight_kg ? Number(e.weight_kg) : null,
        notes: e.notes || null,
      })),
    };

    const url = workoutId ? `/api/workouts/${workoutId}` : "/api/workouts";
    const method = workoutId ? "PUT" : "POST";
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

    router.push(`/workouts/${body.data.id}`);
    router.refresh();
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Details</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Workout name</FormLabel>
                  <FormControl>
                    <Input placeholder="Leg day" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="performed_at"
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
              name="notes"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Notes (optional)</FormLabel>
                  <FormControl>
                    <Input placeholder="How did it feel?" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-base">Exercises</CardTitle>
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="gap-2"
              onClick={() =>
                append({ exercise_id: "", sets: 3, reps: 10, weight_kg: "", notes: "" })
              }
            >
              <Plus className="h-4 w-4" />
              Add exercise
            </Button>
          </CardHeader>
          <CardContent className="space-y-4">
            {fields.length === 0 && (
              <p className="text-sm text-muted-foreground">
                No exercises added yet. Add one to get started.
              </p>
            )}
            {fields.map((field, index) => (
              <div
                key={field.id}
                className="grid grid-cols-2 gap-3 rounded-md border border-border p-4 sm:grid-cols-5"
              >
                <FormField
                  control={form.control}
                  name={`exercises.${index}.exercise_id`}
                  render={({ field }) => (
                    <FormItem className="col-span-2 sm:col-span-2">
                      <FormLabel>Exercise</FormLabel>
                      <Select value={field.value} onValueChange={field.onChange}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select an exercise" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {exercises.map((exercise) => (
                            <SelectItem key={exercise.id} value={exercise.id}>
                              {exercise.name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name={`exercises.${index}.sets`}
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Sets</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          min={1}
                          {...field}
                          value={(field.value as number | string | undefined) ?? ""}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name={`exercises.${index}.reps`}
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Reps</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          min={1}
                          {...field}
                          value={(field.value as number | string | undefined) ?? ""}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name={`exercises.${index}.weight_kg`}
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Weight (kg)</FormLabel>
                      <FormControl>
                        <Input type="number" min={0} step="0.5" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <div className="col-span-2 flex items-end justify-end sm:col-span-5">
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="gap-2"
                    onClick={() => remove(index)}
                  >
                    <Trash2 className="h-4 w-4" />
                    Remove
                  </Button>
                </div>
              </div>
            ))}
            {exercisesErrorMessage && (
              <p className="text-sm font-medium text-destructive">{exercisesErrorMessage}</p>
            )}
          </CardContent>
        </Card>

        {serverError && <p className="text-sm font-medium text-destructive">{serverError}</p>}

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? "Saving…" : workoutId ? "Save changes" : "Create workout"}
        </Button>
      </form>
    </Form>
  );
}
