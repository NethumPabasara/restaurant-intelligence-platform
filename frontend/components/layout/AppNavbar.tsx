"use client";

import { Menu, Bell, Search } from "lucide-react";
import { usePathname } from "next/navigation";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { ThemeToggle } from "@/components/layout/ThemeToggle";
import { navItems } from "@/components/navigation/navItems";
import { cn } from "@/lib/utils";

interface AppNavbarProps {
  onMenuClick?: () => void;
}

export function AppNavbar({ onMenuClick }: AppNavbarProps) {
  const pathname = usePathname();
  const currentTitle = navItems.find((item) => item.href === pathname)?.title ?? "Overview";

  return (
    <header className="flex items-center justify-between rounded-[24px] border border-white/10 bg-white/70 px-4 py-3 shadow-[0_20px_60px_-30px_rgba(15,23,42,0.4)] backdrop-blur-2xl dark:bg-slate-950/70 md:px-6">
      <div className="flex items-center gap-3">
        <Sheet>
          <SheetTrigger
                className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-white/10 bg-white/10 backdrop-blur-xl transition hover:bg-white/20 md:hidden"
            >
                <Menu className="h-4 w-4" />
            </SheetTrigger>
          <SheetContent side="left" className="border-r border-white/10 bg-slate-950/95 p-3 text-white">
            <div className="mt-6 space-y-2">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = pathname === item.href;

                return (
                  <a
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "flex items-center gap-3 rounded-2xl px-3 py-2.5 text-sm font-medium transition",
                      active ? "bg-white/12 text-white" : "text-slate-400 hover:bg-white/8 hover:text-white"
                    )}
                  >
                    <Icon className="h-4 w-4" />
                    {item.title}
                  </a>
                );
              })}
            </div>
          </SheetContent>
        </Sheet>

        <div>
          <p className="text-xs uppercase tracking-[0.28em] text-slate-400">Workspace</p>
          <h1 className="text-lg font-semibold text-foreground">{currentTitle}</h1>
        </div>
      </div>

      <div className="flex items-center gap-2 md:gap-3">
        <label className="hidden items-center gap-2 rounded-full border border-white/10 bg-white/70 px-3 py-2 text-sm text-slate-500 shadow-sm backdrop-blur-xl md:flex dark:bg-slate-900/70 dark:text-slate-400">
          <Search className="h-4 w-4" />
          <Input
            placeholder="Search insights"
            className="h-8 border-none bg-transparent px-0 text-sm shadow-none focus-visible:ring-0"
          />
        </label>

        <Button variant="ghost" size="icon" className="h-10 w-10 rounded-full border border-white/10 bg-white/10 backdrop-blur-xl">
          <Bell className="h-4 w-4" />
        </Button>
        <ThemeToggle />
        <div className="flex items-center gap-3 rounded-full border border-white/10 bg-white/70 px-2 py-2 backdrop-blur-xl dark:bg-slate-900/70">
          <Avatar className="h-9 w-9">
            <AvatarImage src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&q=80" alt="User" />
            <AvatarFallback>AL</AvatarFallback>
          </Avatar>
          <div className="hidden text-left sm:block">
            <p className="text-sm font-medium text-foreground">Alicia Lane</p>
            <p className="text-xs text-slate-500">Operations Lead</p>
          </div>
        </div>
      </div>
    </header>
  );
}
