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
import { measurementSchema, type MeasurementFormValues } from "@/lib/validation/progress";

export function MeasurementForm({
  measurementId,
  defaultValues,
}: {
  measurementId?: string;
  defaultValues?: MeasurementFormValues;
}) {
  const router = useRouter();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<MeasurementFormValues>({
    resolver: zodResolver(measurementSchema),
    defaultValues: defaultValues ?? {
      recorded_at: new Date().toISOString().slice(0, 10),
      weight_kg: "",
      body_fat_pct: "",
      waist_cm: "",
      chest_cm: "",
      hips_cm: "",
      arm_cm: "",
      notes: "",
    },
  });

  async function onSubmit(values: MeasurementFormValues) {
    setServerError(null);
    const toNumber = (v?: string) => (v ? Number(v) : null);
    const payload = {
      recorded_at: values.recorded_at,
      weight_kg: toNumber(values.weight_kg),
      body_fat_pct: toNumber(values.body_fat_pct),
      waist_cm: toNumber(values.waist_cm),
      chest_cm: toNumber(values.chest_cm),
      hips_cm: toNumber(values.hips_cm),
      arm_cm: toNumber(values.arm_cm),
      notes: values.notes || null,
    };

    const url = measurementId ? `/api/measurements/${measurementId}` : "/api/measurements";
    const method = measurementId ? "PUT" : "POST";
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

    router.push("/progress");
    router.refresh();
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Check-in</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <FormField
              control={form.control}
              name="recorded_at"
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
            <div className="grid grid-cols-2 gap-3">
              <FormField
                control={form.control}
                name="weight_kg"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Weight (kg)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} step="0.1" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="body_fat_pct"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Body fat (%)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} max={100} step="0.1" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="waist_cm"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Waist (cm)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} step="0.1" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="chest_cm"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Chest (cm)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} step="0.1" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="hips_cm"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Hips (cm)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} step="0.1" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="arm_cm"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Arm (cm)</FormLabel>
                    <FormControl>
                      <Input type="number" min={0} step="0.1" {...field} />
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
          {form.formState.isSubmitting ? "Saving…" : "Save check-in"}
        </Button>
      </form>
    </Form>
  );
}
