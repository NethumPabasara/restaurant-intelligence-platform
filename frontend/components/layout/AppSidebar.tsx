"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { LayoutGrid, Sparkles } from "lucide-react";
import { navItems } from "@/components/navigation/navItems";
import { cn } from "@/lib/utils";

interface AppSidebarProps {
  collapsed?: boolean;
  onNavigate?: () => void;
}

export function AppSidebar({ collapsed = false, onNavigate }: AppSidebarProps) {
  const pathname = usePathname();

  return (
    <aside className="flex h-full flex-col rounded-[28px] border border-white/10 bg-slate-950/80 p-4 shadow-[0_30px_80px_-30px_rgba(15,23,42,0.75)] backdrop-blur-2xl">
      <div className="flex items-center gap-3 px-2 py-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-400 via-sky-500 to-violet-500 shadow-lg shadow-cyan-500/20">
          <Sparkles className="h-5 w-5 text-white" />
        </div>
        {!collapsed ? (
          <div>
            <p className="text-sm font-semibold text-white">Restaurant AI</p>
            <p className="text-xs text-slate-400">Ops Intelligence</p>
          </div>
        ) : null}
      </div>

      <nav className="mt-8 flex-1 space-y-1.5">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={onNavigate}
              className={cn(
                "group flex items-center gap-3 rounded-2xl px-3 py-2.5 text-sm font-medium transition-all duration-200",
                active
                  ? "bg-white/12 text-white shadow-[inset_0_1px_0_rgba(255,255,255,0.12)]"
                  : "text-slate-400 hover:bg-white/8 hover:text-white"
              )}
            >
              <motion.div
                whileHover={{ scale: 1.04 }}
                whileTap={{ scale: 0.98 }}
                className={cn(
                  "flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/10",
                  active && "bg-gradient-to-br from-cyan-500/20 to-violet-500/20"
                )}
              >
                <Icon className="h-4 w-4" />
              </motion.div>
              {!collapsed ? <span>{item.title}</span> : null}
            </Link>
          );
        })}
      </nav>

      <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-white/10 to-transparent p-3">
        <div className="flex items-center gap-2">
          <LayoutGrid className="h-4 w-4 text-cyan-300" />
          <span className="text-sm font-medium text-white">Live workspace</span>
        </div>
        <p className="mt-2 text-xs text-slate-400">Multi-brand analytics platform</p>
      </div>
    </aside>
  );
}
