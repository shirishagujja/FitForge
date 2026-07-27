"use client";

import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts";

import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

const chartConfig = {
  weight_kg: {
    label: "Weight (kg)",
    color: "hsl(var(--primary))",
  },
} satisfies ChartConfig;

function formatDate(value: string) {
  return new Date(`${value}T00:00:00`).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

export function WeightChart({
  data,
}: {
  data: { recorded_at: string; weight_kg: number }[];
}) {
  return (
    <ChartContainer config={chartConfig} className="aspect-auto h-64 w-full">
      <LineChart data={data} margin={{ left: 12, right: 12, top: 8, bottom: 8 }}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis
          dataKey="recorded_at"
          tickFormatter={formatDate}
          tickLine={false}
          axisLine={false}
          minTickGap={32}
        />
        <YAxis
          tickLine={false}
          axisLine={false}
          width={40}
          domain={["dataMin - 2", "dataMax + 2"]}
        />
        <ChartTooltip
          content={
            <ChartTooltipContent
              labelFormatter={(value) =>
                new Date(`${value}T00:00:00`).toLocaleDateString(undefined, {
                  weekday: "short",
                  month: "short",
                  day: "numeric",
                })
              }
            />
          }
        />
        <Line
          dataKey="weight_kg"
          type="monotone"
          stroke="var(--color-weight_kg)"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ChartContainer>
  );
}
