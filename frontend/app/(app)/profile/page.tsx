import { ProfileForm } from "@/components/profile/ProfileForm";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";
import type { ProfileFormValues } from "@/lib/validation/profile";

export default async function ProfilePage() {
  const response = await serverReadWithAccessToken("/v1/profile");
  let defaultValues: ProfileFormValues | undefined;

  if (response.ok) {
    const profile = (await response.json()).data;
    defaultValues = {
      display_name: profile.display_name ?? "",
      date_of_birth: profile.date_of_birth ?? "",
      sex: profile.sex ?? undefined,
      height_cm: profile.height_cm?.toString() ?? "",
      fitness_goal: profile.fitness_goal ?? "",
      activity_level: profile.activity_level ?? undefined,
    };
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="mb-6 text-2xl font-bold tracking-tight">Profile</h1>
      <ProfileForm defaultValues={defaultValues} />
    </div>
  );
}
