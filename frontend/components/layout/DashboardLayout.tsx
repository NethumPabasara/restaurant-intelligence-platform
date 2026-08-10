"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { AppNavbar } from "@/components/layout/AppNavbar";
import { AppSidebar } from "@/components/layout/AppSidebar";
import { cn } from "@/lib/utils";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(34,211,238,0.18),_transparent_32%),radial-gradient(circle_at_top_right,_rgba(129,140,248,0.2),_transparent_28%),linear-gradient(135deg,_rgba(2,6,23,0.98)_0%,_rgba(15,23,42,0.96)_100%)] px-3 py-3 text-foreground sm:px-4 lg:px-6 lg:py-6">
      <div className="mx-auto flex max-w-7xl gap-4">
        <motion.aside
          initial={false}
          animate={{ width: collapsed ? 88 : 280 }}
          transition={{ duration: 0.25, ease: "easeOut" }}
          className="hidden lg:block"
        >
          <AppSidebar collapsed={collapsed} onNavigate={() => setCollapsed(false)} />
        </motion.aside>

        <div className="flex min-h-[calc(100vh-1.5rem)] flex-1 flex-col gap-4">
          <AppNavbar />

          <motion.main
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className={cn(
              "flex-1 rounded-[30px] border border-white/10 bg-white/70 p-5 shadow-[0_30px_80px_-30px_rgba(15,23,42,0.55)] backdrop-blur-2xl dark:bg-slate-950/70",
              collapsed && "lg:ml-0"
            )}
          >
            {children}
          </motion.main>
        </div>
      </div>
    </div>
  );
}
