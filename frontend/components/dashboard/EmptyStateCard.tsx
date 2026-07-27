import type { LucideIcon } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export function EmptyStateCard({
  icon: Icon,
  title,
  description,
  ctaLabel,
}: {
  icon: LucideIcon;
  title: string;
  description: string;
  ctaLabel: string;
}) {
  return (
    <Card>
      <CardHeader>
        <div className="mb-2 flex h-9 w-9 items-center justify-center rounded-md bg-muted">
          <Icon className="h-5 w-5 text-muted-foreground" />
        </div>
        <CardTitle className="text-base">{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent>
        <Button variant="outline" size="sm" disabled className="gap-2">
          {ctaLabel}
          <Badge variant="secondary" className="text-[10px]">
            Soon
          </Badge>
        </Button>
      </CardContent>
    </Card>
  );
}
