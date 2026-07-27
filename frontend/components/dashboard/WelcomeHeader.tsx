function getGreeting(date: Date): string {
  const hour = date.getHours();
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}

export function WelcomeHeader({ name }: { name: string }) {
  const now = new Date();
  const dateLabel = now.toLocaleDateString(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric",
  });

  return (
    <div>
      <p className="text-sm text-muted-foreground">{dateLabel}</p>
      <h1 className="text-2xl font-bold tracking-tight">
        {getGreeting(now)}, {name}
      </h1>
    </div>
  );
}
