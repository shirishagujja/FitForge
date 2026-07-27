import { z } from "zod";

export const workoutExerciseSchema = z.object({
  exercise_id: z.string().min(1, "Select an exercise"),
  sets: z.coerce.number().int().min(1, "At least 1 set").max(50, "Max 50 sets"),
  reps: z.coerce.number().int().min(1, "At least 1 rep").max(1000, "Max 1000 reps"),
  weight_kg: z.string().optional(),
  notes: z.string().max(500).optional(),
});

export const workoutSchema = z.object({
  name: z.string().min(1, "Name is required").max(255),
  performed_at: z.string().min(1, "Date is required"),
  notes: z.string().max(2000).optional(),
  exercises: z.array(workoutExerciseSchema).min(1, "Add at least one exercise"),
});

// sets/reps use z.coerce, so the pre-parse (input) and post-parse (output) shapes differ —
// react-hook-form needs both: input for form state/defaultValues, output for onSubmit.
export type WorkoutFormInput = z.input<typeof workoutSchema>;
export type WorkoutFormValues = z.output<typeof workoutSchema>;
