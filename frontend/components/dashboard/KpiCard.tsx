import { ArrowUpRight, ArrowDownRight, Minus } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import type { KpiCardData } from "./types";

interface KpiCardProps {
  item: KpiCardData;
}

export function KpiCard({ item }: KpiCardProps) {
  const Icon = item.icon;
  const trendClasses = {
    up: "bg-emerald-500/10 text-emerald-400",
    down: "bg-rose-500/10 text-rose-400",
    neutral: "bg-slate-500/10 text-slate-400",
  };

  const trendIcon = {
    up: ArrowUpRight,
    down: ArrowDownRight,
    neutral: Minus,
  };

  const TrendIcon = trendIcon[item.trendDirection];

  return (
    <Card className="group relative overflow-hidden border-white/10 bg-white/5 shadow-[0_0_0_1px_rgba(255,255,255,0.03)] backdrop-blur-xl">
      <CardContent className="flex items-start justify-between gap-4 p-5">
        <div className="flex-1 space-y-3">
          <div className="flex items-center gap-2 text-sm text-slate-400">
            <span>{item.title}</span>
            {item.tooltip ? (
              <span className="text-xs text-slate-500">• {item.tooltip}</span>
            ) : null}
          </div>
          <div className="text-3xl font-semibold tracking-tight text-white">
            {item.value}
          </div>
          <div className="flex items-center gap-2">
            <Badge
              variant="secondary"
              className={cn("border-0 px-2.5 py-1 text-xs", trendClasses[item.trendDirection])}
            >
              <TrendIcon className="size-3.5" />
              {item.percentageTrend}
            </Badge>
            <span className="text-xs text-slate-500">vs last period</span>
          </div>
        </div>
        <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-3 text-cyan-400 shadow-inner shadow-cyan-500/10">
          <Icon className="size-5" />
        </div>
      </CardContent>
    </Card>
  );
}
