import type { LucideIcon } from "lucide-react";

export type TrendDirection = "up" | "down" | "neutral";

export interface KpiCardData {
  title: string;
  value: string;
  percentageTrend: string;
  trendDirection: TrendDirection;
  icon: LucideIcon;
  tooltip?: string;
  loading?: boolean;
}

export interface RevenuePoint {
  label: string;
  value: number;
}

export interface ExecutiveSummaryCardData {
  title: string;
  value: string;
  description?: string;
}

export interface InsightItem {
  title: string;
  description: string;
  accent?: "cyan" | "violet" | "emerald";
}

export interface MetricListItem {
  label: string;
  value: string;
  detail?: string;
  tone?: TrendDirection;
}
