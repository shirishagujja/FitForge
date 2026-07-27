import { Dumbbell, MessageCircle, Salad, Sparkles } from "lucide-react";
import Link from "next/link";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { serverReadWithAccessToken } from "@/lib/auth/authedFetch";

type RecommendationsData = { recommendations: string[] };

export default async function AiHubPage() {
  const response = await serverReadWithAccessToken("/v1/ai/recommendations");
  const recommendations: string[] = response.ok
    ? ((await response.json()).data as RecommendationsData).recommendations
    : [];

  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">AI Coach</h1>
        <p className="text-sm text-muted-foreground">
          Personalized workout ideas, meal suggestions, and a coach to chat with.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Sparkles className="h-4 w-4" />
            Recommendations
          </CardTitle>
        </CardHeader>
        <CardContent>
          {recommendations.length === 0 ? (
            <p className="text-sm text-muted-foreground">
              Log a few workouts and meals to get personalized recommendations.
            </p>
          ) : (
            <ul className="list-inside list-disc space-y-1 text-sm text-muted-foreground">
              {recommendations.map((rec, index) => (
                <li key={index}>{rec}</li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-4 sm:grid-cols-3">
        <Link href="/ai/workout">
          <Card className="h-full transition-colors hover:bg-accent">
            <CardHeader>
              <Dumbbell className="mb-2 h-6 w-6 text-muted-foreground" />
              <CardTitle className="text-base">Generate a workout</CardTitle>
              <CardDescription>Tell us your goal, we&apos;ll build a plan.</CardDescription>
            </CardHeader>
          </Card>
        </Link>
        <Link href="/ai/meals">
          <Card className="h-full transition-colors hover:bg-accent">
            <CardHeader>
              <Salad className="mb-2 h-6 w-6 text-muted-foreground" />
              <CardTitle className="text-base">Get meal ideas</CardTitle>
              <CardDescription>Suggestions that fit your calorie target.</CardDescription>
            </CardHeader>
          </Card>
        </Link>
        <Link href="/ai/chat">
          <Card className="h-full transition-colors hover:bg-accent">
            <CardHeader>
              <MessageCircle className="mb-2 h-6 w-6 text-muted-foreground" />
              <CardTitle className="text-base">Chat with your coach</CardTitle>
              <CardDescription>Ask anything about training or nutrition.</CardDescription>
            </CardHeader>
          </Card>
        </Link>
      </div>
    </div>
  );
}
