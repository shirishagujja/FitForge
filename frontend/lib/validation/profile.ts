import { z } from "zod";

export const profileSchema = z.object({
  display_name: z.string().max(100).optional(),
  date_of_birth: z.string().optional(),
  sex: z.enum(["male", "female", "unspecified"]).optional(),
  height_cm: z.string().optional(),
  fitness_goal: z.string().max(255).optional(),
  activity_level: z
    .enum(["sedentary", "light", "moderate", "active", "very_active"])
    .optional(),
});

export type ProfileFormValues = z.infer<typeof profileSchema>;
