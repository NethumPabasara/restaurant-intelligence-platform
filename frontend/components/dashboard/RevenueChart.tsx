import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { RevenuePoint } from "./types";

interface RevenueChartProps {
  data: RevenuePoint[];
}

export function RevenueChart({ data }: RevenueChartProps) {
  const maxValue = Math.max(...data.map((item) => item.value));

  return (
    <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
      <CardHeader className="pb-3">
        <CardTitle className="text-base text-white">Revenue momentum</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex h-52 items-end gap-3 rounded-2xl border border-white/10 bg-slate-950/60 p-4">
          {data.map((item, index) => (
            <div key={`${item.label}-${index}`} className="flex flex-1 flex-col items-center gap-3">
              <div className="flex h-full w-full items-end">
                <div
                  className="w-full rounded-t-2xl bg-gradient-to-t from-cyan-500 via-cyan-400 to-violet-500 shadow-[0_0_30px_rgba(34,211,238,0.24)]"
                  style={{ height: `${(item.value / maxValue) * 100}%` }}
                />
              </div>
              <div className="text-center text-xs text-slate-400">
                <div className="font-medium text-slate-300">{item.label}</div>
                <div className="text-[11px] text-slate-500">{item.value}k</div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
