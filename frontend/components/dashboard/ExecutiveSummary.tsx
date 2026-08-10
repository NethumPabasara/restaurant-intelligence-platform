import { Card, CardContent } from "@/components/ui/card";
import type { ExecutiveSummaryCardData } from "./types";

interface ExecutiveSummaryProps {
  items: ExecutiveSummaryCardData[];
}

export function ExecutiveSummary({ items }: ExecutiveSummaryProps) {
  return (
    <div className="grid gap-3 md:grid-cols-3">
      {items.map((item) => (
        <Card key={item.title} className="border-white/10 bg-white/5 backdrop-blur-xl">
          <CardContent className="space-y-2 p-4">
            <div className="text-sm text-slate-400">{item.title}</div>
            <div className="text-2xl font-semibold text-white">{item.value}</div>
            {item.description ? (
              <div className="text-sm text-slate-500">{item.description}</div>
            ) : null}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
