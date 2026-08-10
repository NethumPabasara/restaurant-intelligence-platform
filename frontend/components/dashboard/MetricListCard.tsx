import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { MetricListItem } from "./types";

interface MetricListCardProps {
  title: string;
  description: string;
  items: MetricListItem[];
  accent?: "cyan" | "violet" | "emerald";
}

const accentClasses = {
  cyan: "text-cyan-300",
  violet: "text-violet-300",
  emerald: "text-emerald-300",
};

export function MetricListCard({ title, description, items, accent = "cyan" }: MetricListCardProps) {
  return (
    <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
      <CardHeader className="pb-3">
        <CardTitle className="text-base text-white">{title}</CardTitle>
        <p className="text-sm leading-6 text-slate-400">{description}</p>
      </CardHeader>
      <CardContent className="space-y-3">
        {items.map((item) => (
          <div key={item.label} className="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="text-sm text-slate-400">{item.label}</div>
                <div className={cn("mt-1 text-xl font-semibold text-white", accentClasses[accent])}>{item.value}</div>
              </div>
              {item.tone ? (
                <Badge
                  variant="outline"
                  className={cn(
                    "border-0 px-2.5 py-1 text-xs",
                    item.tone === "up" && "bg-emerald-500/10 text-emerald-400",
                    item.tone === "down" && "bg-rose-500/10 text-rose-400",
                    item.tone === "neutral" && "bg-slate-500/10 text-slate-400"
                  )}
                >
                  {item.tone === "up" ? "+" : item.tone === "down" ? "-" : "•"}
                </Badge>
              ) : null}
            </div>
            {item.detail ? <div className="mt-2 text-sm text-slate-500">{item.detail}</div> : null}
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
