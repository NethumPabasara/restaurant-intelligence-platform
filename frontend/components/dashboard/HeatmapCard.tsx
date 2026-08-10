import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface HeatmapRow {
  label: string;
  values: Array<string | number>;
}

interface HeatmapCardProps {
  title: string;
  description: string;
  rows: HeatmapRow[];
}

export function HeatmapCard({ title, description, rows }: HeatmapCardProps) {
  return (
    <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
      <CardHeader className="pb-3">
        <CardTitle className="text-base text-white">{title}</CardTitle>
        <p className="text-sm leading-6 text-slate-400">{description}</p>
      </CardHeader>
      <CardContent>
        <div className="overflow-hidden rounded-2xl border border-white/10 bg-slate-950/60 p-3">
          <div className="grid grid-cols-[auto_repeat(7,minmax(0,1fr))] gap-2 text-xs text-slate-500">
            <div />
            {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day) => (
              <div key={day} className="text-center text-[11px] uppercase tracking-[0.2em] text-slate-500">
                {day}
              </div>
            ))}
            {rows.map((row) => (
              <div key={row.label} className="contents">
                <div className="flex items-center text-sm text-slate-400">
                  {row.label}
                </div>
                {row.values.map((value) => {
                  const numeric = Number(value);
                  let color = "bg-slate-800/80 text-slate-400";
                  if (numeric >= 90) color = "bg-emerald-500/20 text-emerald-300";
                  else if (numeric >= 80) color = "bg-cyan-500/20 text-cyan-300";
                  else if (numeric >= 70) color = "bg-violet-500/20 text-violet-300";
                  else color = "bg-slate-700/70 text-slate-400";

                  return (
                    <div key={`${row.label}-${value}`} className={`flex h-10 items-center justify-center rounded-xl border border-white/10 ${color}`}>
                      {value}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
