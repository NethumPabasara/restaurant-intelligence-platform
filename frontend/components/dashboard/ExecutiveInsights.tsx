import { Sparkles, BrainCircuit, ShieldCheck } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { InsightItem } from "./types";

interface ExecutiveInsightsProps {
  items: InsightItem[];
}

const iconMap = {
  cyan: Sparkles,
  violet: BrainCircuit,
  emerald: ShieldCheck,
};

export function ExecutiveInsights({ items }: ExecutiveInsightsProps) {
  return (
    <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base text-white">Executive insights</CardTitle>
          <Badge variant="outline" className="border-cyan-400/20 bg-cyan-400/10 text-cyan-300">
            AI summary
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {items.map((item) => {
          const Icon = iconMap[item.accent ?? "cyan"];
          return (
            <div key={item.title} className="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
              <div className="mb-2 flex items-center gap-2">
                <div className="rounded-xl border border-white/10 bg-white/10 p-2 text-cyan-300">
                  <Icon className="size-4" />
                </div>
                <h3 className="text-sm font-semibold text-white">{item.title}</h3>
              </div>
              <p className="text-sm leading-6 text-slate-400">{item.description}</p>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}
