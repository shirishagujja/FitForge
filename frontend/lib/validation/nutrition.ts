import { z } from "zod";

export const mealSchema = z.object({
  name: z.string().min(1, "Name is required").max(255),
  logged_at: z.string().min(1, "Date is required"),
  calories: z.coerce.number().int().min(0, "Must be 0 or more").max(20000),
  protein_g: z.string().optional(),
  carbs_g: z.string().optional(),
  fat_g: z.string().optional(),
  notes: z.string().max(500).optional(),
});

export type MealFormInput = z.input<typeof mealSchema>;
export type MealFormValues = z.output<typeof mealSchema>;
