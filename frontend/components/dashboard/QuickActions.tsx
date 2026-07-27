import { Dumbbell, Salad, UserCog } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const actions = [
  { label: "Log a workout", icon: Dumbbell },
  { label: "Log a meal", icon: Salad },
  { label: "Update profile", icon: UserCog },
];

export function QuickActions() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base">Quick actions</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-wrap gap-3">
        {actions.map((action) => (
          <Button key={action.label} variant="outline" disabled className="gap-2">
            <action.icon className="h-4 w-4" />
            {action.label}
            <Badge variant="secondary" className="text-[10px]">
              Soon
            </Badge>
          </Button>
        ))}
      </CardContent>
    </Card>
  );
}
