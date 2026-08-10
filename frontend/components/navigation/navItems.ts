import type { LucideIcon } from "lucide-react";
import {
  BarChart3,
  Boxes,
  Compass,
  DollarSign,
  Settings2,
  ShoppingBag,
} from "lucide-react";

export interface NavItem {
  title: string;
  href: string;
  icon: LucideIcon;
}

export const navItems: NavItem[] = [
  {
    title: "Executive Dashboard",
    href: "/executive",
    icon: BarChart3,
  },
  {
    title: "Sales Dashboard",
    href: "/sales",
    icon: ShoppingBag,
  },
  {
    title: "Product Dashboard",
    href: "/product",
    icon: Boxes,
  },
  {
    title: "Channel Dashboard",
    href: "/channel",
    icon: Compass,
  },
  {
    title: "Financial Dashboard",
    href: "/financial",
    icon: DollarSign,
  },
  {
    title: "Settings",
    href: "/settings",
    icon: Settings2,
  },
];
