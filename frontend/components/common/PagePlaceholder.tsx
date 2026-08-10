import { Sparkles } from "lucide-react";

interface PagePlaceholderProps {
  title: string;
}

export function PagePlaceholder({ title }: PagePlaceholderProps) {
  return (
    <div className="flex min-h-[480px] flex-col items-center justify-center rounded-[24px] border border-dashed border-white/15 bg-gradient-to-br from-white/50 to-transparent p-10 text-center shadow-inner shadow-white/5 dark:from-white/10">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500/20 via-sky-500/20 to-violet-500/20">
        <Sparkles className="h-6 w-6 text-cyan-400" />
      </div>
      <h2 className="text-2xl font-semibold tracking-tight text-foreground">{title}</h2>
      <p className="mt-2 max-w-md text-sm text-slate-500 dark:text-slate-400">
        This placeholder route is ready for the upcoming dashboard experience.
      </p>
    </div>
  );
}
