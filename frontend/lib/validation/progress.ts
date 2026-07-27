import { z } from "zod";

export const measurementSchema = z.object({
  recorded_at: z.string().min(1, "Date is required"),
  weight_kg: z.string().optional(),
  body_fat_pct: z.string().optional(),
  waist_cm: z.string().optional(),
  chest_cm: z.string().optional(),
  hips_cm: z.string().optional(),
  arm_cm: z.string().optional(),
  notes: z.string().max(500).optional(),
});

export type MeasurementFormValues = z.infer<typeof measurementSchema>;

export const goalSchema = z.object({
  title: z.string().min(1, "Title is required").max(255),
  target_weight_kg: z.string().optional(),
  target_date: z.string().optional(),
});

export type GoalFormValues = z.infer<typeof goalSchema>;
