"use client";

import { useEffect, useState } from "react";
import {
  ArrowRightLeft,
  BarChart3,
  BrainCircuit,
  DollarSign,
  Sparkles,
  TrendingUp,
  Users,
} from "lucide-react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { ExecutiveInsights } from "@/components/dashboard/ExecutiveInsights";
import { ExecutiveSummary } from "@/components/dashboard/ExecutiveSummary";
import { HeatmapCard } from "@/components/dashboard/HeatmapCard";
import { KpiCard } from "@/components/dashboard/KpiCard";
import { MetricListCard } from "@/components/dashboard/MetricListCard";
import { RevenueChart } from "@/components/dashboard/RevenueChart";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { fetchExecutiveDashboard } from "@/lib/api";
import type {
  ExecutiveSummaryCardData,
  InsightItem,
  KpiCardData,
  MetricListItem,
  RevenuePoint,
} from "@/components/dashboard/types";

interface ExecutiveDashboardResponse {
  cards: {
    total_revenue: number;
    total_profit: number;
    total_orders: number;
    average_order_value: number;
    profit_margin: number;
  };
  revenue_trend: Array<{ month: string; revenue: number }>;
  profit_trend: Array<{ month: string; profit: number }>;
  business_channel_revenue: Array<{ channel: string; revenue: number }>;
  monthly_channel_revenue: Array<Record<string, string | number>>;
  revenue_growth: Array<{ month: string; revenue: number; growth: number }>;
  top_performing_month: { month: string; revenue: number };
  lowest_performing_month: { month: string; revenue: number };
  best_sales_day: { date: string; revenue: number };
  worst_sales_day: { date: string; revenue: number };
  revenue_by_weekday: Array<{ weekday: string; revenue: number }>;
  revenue_heatmap: Array<{ month: string; weekday: string; revenue: number }>;
  executive_summary: {
    business_status: string;
    revenue_summary: string;
    profit_summary: string;
    sales_summary: string;
    risk_summary: string;
    recommendation: string;
  };
  executive_health_score: { score: number; status: string; color: string };
  ai_business_insights: string[];
}

function formatCompactCurrency(value: number) {
  if (value >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(2)}M`;
  }

  if (value >= 1_000) {
    return `$${(value / 1_000).toFixed(1)}K`;
  }

  return `$${value.toFixed(0)}`;
}

function formatCompactNumber(value: number) {
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(1)}M`;
  }

  if (value >= 1_000) {
    return `${(value / 1_000).toFixed(1)}K`;
  }

  return value.toFixed(0);
}

function formatPercent(value: number) {
  return `${value.toFixed(1)}%`;
}

function getTrendDirection(value: number): "up" | "down" | "neutral" {
  if (value > 0) {
    return "up";
  }

  if (value < 0) {
    return "down";
  }

  return "neutral";
}

function buildKpiCards(data: ExecutiveDashboardResponse | null): KpiCardData[] {
  if (!data) {
    return [
      { title: "Revenue", value: "—", percentageTrend: "—", trendDirection: "neutral", icon: DollarSign, tooltip: "Loading" },
      { title: "Order volume", value: "—", percentageTrend: "—", trendDirection: "neutral", icon: BarChart3, tooltip: "Loading" },
      { title: "Average ticket", value: "—", percentageTrend: "—", trendDirection: "neutral", icon: ArrowRightLeft, tooltip: "Loading" },
      { title: "Profit margin", value: "—", percentageTrend: "—", trendDirection: "neutral", icon: Users, tooltip: "Loading" },
    ];
  }

  const latestGrowth = data.revenue_growth[data.revenue_growth.length - 1]?.growth ?? 0;

  return [
    {
      title: "Revenue",
      value: formatCompactCurrency(data.cards.total_revenue),
      percentageTrend: `${latestGrowth >= 0 ? "+" : ""}${latestGrowth.toFixed(1)}%`,
      trendDirection: getTrendDirection(latestGrowth),
      icon: DollarSign,
      tooltip: "Live API data",
    },
    {
      title: "Order volume",
      value: formatCompactNumber(data.cards.total_orders),
      percentageTrend: `${latestGrowth >= 0 ? "+" : ""}${latestGrowth.toFixed(1)}%`,
      trendDirection: getTrendDirection(latestGrowth),
      icon: BarChart3,
      tooltip: "Live API data",
    },
    {
      title: "Average ticket",
      value: formatCompactCurrency(data.cards.average_order_value),
      percentageTrend: `${latestGrowth >= 0 ? "+" : ""}${latestGrowth.toFixed(1)}%`,
      trendDirection: getTrendDirection(latestGrowth),
      icon: ArrowRightLeft,
      tooltip: "Live API data",
    },
    {
      title: "Profit margin",
      value: formatPercent(data.cards.profit_margin),
      percentageTrend: `${latestGrowth >= 0 ? "+" : ""}${latestGrowth.toFixed(1)}%`,
      trendDirection: getTrendDirection(latestGrowth),
      icon: Users,
      tooltip: "Live API data",
    },
  ];
}

function buildRevenueData(data: ExecutiveDashboardResponse | null): RevenuePoint[] {
  if (!data) {
    return [];
  }

  return data.revenue_trend.map((item) => ({
    label: item.month.slice(0, 3),
    value: Number(item.revenue.toFixed(0)),
  }));
}

function buildSummaryCards(data: ExecutiveDashboardResponse | null): ExecutiveSummaryCardData[] {
  if (!data) {
    return [];
  }

  return [
    {
      title: "Business status",
      value: data.executive_summary.business_status,
      description: data.executive_summary.recommendation,
    },
    {
      title: "Revenue summary",
      value: data.executive_summary.revenue_summary,
      description: data.executive_summary.profit_summary,
    },
    {
      title: "Risk outlook",
      value: data.executive_health_score.status,
      description: data.executive_summary.risk_summary,
    },
  ];
}

function buildInsightItems(data: ExecutiveDashboardResponse | null): InsightItem[] {
  if (!data) {
    return [];
  }

  return data.ai_business_insights.map((insight, index) => ({
    title: `Insight ${index + 1}`,
    description: insight,
    accent: (index % 3 === 0 ? "cyan" : index % 3 === 1 ? "violet" : "emerald") as InsightItem["accent"],
  }));
}

function buildProfitTrendItems(data: ExecutiveDashboardResponse | null): MetricListItem[] {
  if (!data) {
    return [];
  }

  const latest = data.profit_trend[data.profit_trend.length - 1];
  const previous = data.profit_trend[data.profit_trend.length - 2];
  const trend = previous ? ((latest.profit - previous.profit) / previous.profit) * 100 : 0;

  return [
    {
      label: "Profit trend",
      value: formatCompactCurrency(latest.profit),
      detail: `${latest.month} vs ${previous?.month ?? "previous"}`,
      tone: getTrendDirection(trend),
    },
    {
      label: "Contribution margin",
      value: formatPercent(data.cards.profit_margin),
      detail: "Current profitability signal",
      tone: data.cards.profit_margin >= 30 ? "up" : "neutral",
    },
    {
      label: "Cost pressure",
      value: data.cards.profit_margin >= 30 ? "Low" : "Elevated",
      detail: "Derived from live margin performance",
      tone: data.cards.profit_margin >= 30 ? "up" : "down",
    },
  ];
}

function buildChannelRevenueItems(data: ExecutiveDashboardResponse | null): MetricListItem[] {
  if (!data) {
    return [];
  }

  return data.business_channel_revenue.map((item) => ({
    label: item.channel,
    value: formatCompactCurrency(item.revenue),
    detail: "Live channel contribution",
    tone: item.revenue >= 0 ? "up" : "neutral",
  }));
}

function buildMonthlyRevenueItems(data: ExecutiveDashboardResponse | null): MetricListItem[] {
  if (!data) {
    return [];
  }

  const latest = data.monthly_channel_revenue[data.monthly_channel_revenue.length - 1];
  const latestMonth = String(latest?.Month ?? "Latest");
  const totalRevenue = data.cards.total_revenue;

  return [
    {
      label: "Latest month",
      value: latestMonth,
      detail: "Current monthly channel view",
      tone: "up",
    },
    {
      label: "Total revenue",
      value: formatCompactCurrency(totalRevenue),
      detail: "Rolling business total",
      tone: "up",
    },
    {
      label: "Channel mix",
      value: `${data.business_channel_revenue.length} channels`,
      detail: "Updated from API response",
      tone: "neutral",
    },
  ];
}

function buildGrowthItems(data: ExecutiveDashboardResponse | null): MetricListItem[] {
  if (!data) {
    return [];
  }

  const latest = data.revenue_growth[data.revenue_growth.length - 1];

  return [
    {
      label: "Revenue growth",
      value: `${latest.growth >= 0 ? "+" : ""}${latest.growth.toFixed(1)}%`,
      detail: latest.month,
      tone: getTrendDirection(latest.growth),
    },
    {
      label: "Latest revenue",
      value: formatCompactCurrency(latest.revenue),
      detail: "Most recent month",
      tone: getTrendDirection(latest.growth),
    },
    {
      label: "Momentum",
      value: latest.growth >= 0 ? "Positive" : "Mixed",
      detail: "Derived from the revenue trend",
      tone: getTrendDirection(latest.growth),
    },
  ];
}

function buildWeekdayItems(data: ExecutiveDashboardResponse | null): MetricListItem[] {
  if (!data) {
    return [];
  }

  const sorted = [...data.revenue_by_weekday].sort((a, b) => b.revenue - a.revenue);
  const top = sorted[0];
  const bottom = sorted[sorted.length - 1];

  return [
    {
      label: "Highest day",
      value: top?.weekday ?? "—",
      detail: `${formatCompactCurrency(top?.revenue ?? 0)} in sales`,
      tone: "up",
    },
    {
      label: "Lowest day",
      value: bottom?.weekday ?? "—",
      detail: `${formatCompactCurrency(bottom?.revenue ?? 0)} in sales`,
      tone: "down",
    },
    {
      label: "Weekly rhythm",
      value: `${data.revenue_by_weekday.length} days`,
      detail: "Mapped from the API weekday data",
      tone: "neutral",
    },
  ];
}

function buildHealthScoreItems(data: ExecutiveDashboardResponse | null): MetricListItem[] {
  if (!data) {
    return [];
  }

  return [
    {
      label: "Executive health score",
      value: `${data.executive_health_score.score}/100`,
      detail: data.executive_health_score.status,
      tone: "up",
    },
    {
      label: "Risk level",
      value: data.executive_health_score.color,
      detail: "Derived from the backend score",
      tone: data.executive_health_score.color === "green" ? "up" : "neutral",
    },
    {
      label: "Readiness",
      value: data.executive_health_score.status,
      detail: "Updated from live executive metrics",
      tone: "up",
    },
  ];
}

function buildHeatmapRows(data: ExecutiveDashboardResponse | null) {
  if (!data) {
    return [];
  }

  const monthOrder = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const weekdayOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  const grouped = monthOrder
    .map((month) => ({
      label: month,
      values: weekdayOrder.map((weekday) => {
        const match = data.revenue_heatmap.find((item) => item.month === month && item.weekday === weekday);
        return match ? Number(match.revenue.toFixed(0)) : 0;
      }),
    }))
    .filter((row) => row.values.some((value) => value > 0));

  return grouped;
}

function buildMonthCards(data: ExecutiveDashboardResponse | null): MetricListItem[] {
  if (!data) {
    return [];
  }

  return [
    {
      label: "Top month",
      value: data.top_performing_month.month,
      detail: formatCompactCurrency(data.top_performing_month.revenue),
      tone: "up",
    },
    {
      label: "Lowest month",
      value: data.lowest_performing_month.month,
      detail: formatCompactCurrency(data.lowest_performing_month.revenue),
      tone: "down",
    },
    {
      label: "Spread",
      value: `${Math.round(((data.top_performing_month.revenue - data.lowest_performing_month.revenue) / data.lowest_performing_month.revenue) * 100)}%`,
      detail: "Difference between peak and trough",
      tone: "neutral",
    },
  ];
}

function buildSalesDayCards(data: ExecutiveDashboardResponse | null): MetricListItem[] {
  if (!data) {
    return [];
  }

  return [
    {
      label: "Best day",
      value: data.best_sales_day.date,
      detail: formatCompactCurrency(data.best_sales_day.revenue),
      tone: "up",
    },
    {
      label: "Worst day",
      value: data.worst_sales_day.date,
      detail: formatCompactCurrency(data.worst_sales_day.revenue),
      tone: "down",
    },
    {
      label: "Gap",
      value: `${Math.round(((data.best_sales_day.revenue - data.worst_sales_day.revenue) / data.worst_sales_day.revenue) * 100)}%`,
      detail: "Gap between top and bottom day",
      tone: "neutral",
    },
  ];
}

export default function ExecutivePage() {
  const [dashboardData, setDashboardData] = useState<ExecutiveDashboardResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadDashboardData() {
      setIsLoading(true);
      setError(null);

      try {
  const data = await fetchExecutiveDashboard();

  console.log("API DATA:", data);

  if (isMounted) {
    setDashboardData(data);
  }
} catch (err) {
  console.error("EXECUTIVE ERROR:", err);

  if (isMounted) {
    setError(String(err));
  }
}
    }

    loadDashboardData();

    return () => {
      isMounted = false;
    };
  }, []);

  const kpiData = buildKpiCards(dashboardData);
  const revenueData = buildRevenueData(dashboardData);
  const summaryCards = buildSummaryCards(dashboardData);
  const insightItems = buildInsightItems(dashboardData);
  const profitTrendItems = buildProfitTrendItems(dashboardData);
  const channelRevenueItems = buildChannelRevenueItems(dashboardData);
  const monthlyRevenueItems = buildMonthlyRevenueItems(dashboardData);
  const growthItems = buildGrowthItems(dashboardData);
  const weekdayItems = buildWeekdayItems(dashboardData);
  const healthScoreItems = buildHealthScoreItems(dashboardData);
  const heatmapRows = buildHeatmapRows(dashboardData);
  const monthCards = buildMonthCards(dashboardData);
  const salesDayCards = buildSalesDayCards(dashboardData);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex flex-col gap-4 rounded-[32px] border border-white/10 bg-gradient-to-br from-slate-900/80 via-slate-900/70 to-cyan-950/40 p-6 shadow-[0_0_0_1px_rgba(255,255,255,0.03)] backdrop-blur-xl md:flex-row md:items-end md:justify-between">
          <div className="space-y-3">
            <div className="flex items-center gap-2 text-sm text-cyan-300">
              <Sparkles className="size-4" />
              <span>Executive command center</span>
            </div>
            <div className="space-y-2">
              <h1 className="text-3xl font-semibold tracking-tight text-white">
                Premium performance overview
              </h1>
              <p className="max-w-2xl text-sm leading-6 text-slate-400">
                A premium, mock-ready executive snapshot designed to scale from prototype to live KPI streams.
              </p>
            </div>
          </div>
          <Badge variant="outline" className="w-fit border-cyan-400/20 bg-cyan-400/10 text-cyan-200">
            <TrendingUp className="mr-2 size-3.5" />
            {isLoading ? "Loading live data" : error ? "Data unavailable" : "Live outlook: improving"}
          </Badge>
        </div>

        {isLoading ? (
          <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
            <CardContent className="p-4 text-sm text-slate-400">
              Loading executive dashboard data from the backend endpoint.
            </CardContent>
          </Card>
        ) : null}

        {error ? (
          <Card className="border-rose-500/20 bg-rose-500/10 backdrop-blur-xl">
            <CardContent className="p-4 text-sm text-rose-200">
              {error}
            </CardContent>
          </Card>
        ) : null}

        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {kpiData.map((item) => (
            <KpiCard key={item.title} item={item} />
          ))}
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.7fr_0.9fr]">
          <RevenueChart data={revenueData} />
          <ExecutiveInsights items={insightItems} />
        </div>

        <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
          <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
            <CardHeader className="pb-3">
              <CardTitle className="text-base text-white">Business performance</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-2xl border border-white/10 bg-slate-950/60 p-4">
                <div className="mb-3 flex items-center gap-2 text-sm text-slate-400">
                  <BrainCircuit className="size-4 text-cyan-300" />
                  <span>Channel mix and margin quality</span>
                </div>
                <div className="grid gap-3 sm:grid-cols-2">
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="text-sm text-slate-400">Digital mix</div>
                    <div className="mt-2 text-2xl font-semibold text-white">{dashboardData ? formatPercent(dashboardData.cards.profit_margin) : "—"}</div>
                    <div className="mt-1 text-sm text-emerald-400">{dashboardData ? "Updated from API" : "Awaiting data"}</div>
                  </div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-4">
                    <div className="text-sm text-slate-400">Premium mix</div>
                    <div className="mt-2 text-2xl font-semibold text-white">{dashboardData ? `${dashboardData.business_channel_revenue.length} channels` : "—"}</div>
                    <div className="mt-1 text-sm text-cyan-400">{dashboardData ? "Live channel data" : "Awaiting data"}</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <div className="space-y-4">
            <ExecutiveSummary items={summaryCards} />
            <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
              <CardContent className="p-4">
                <div className="flex items-center justify-between text-sm text-slate-400">
                  <span>Forecast confidence</span>
                  <span className="text-emerald-400">{dashboardData ? dataStatus(dashboardData) : "—"}</span>
                </div>
                <div className="mt-3 h-2 rounded-full bg-slate-800">
                  <div className="h-2 w-[78%] rounded-full bg-gradient-to-r from-cyan-400 to-violet-500" />
                </div>
                <p className="mt-3 text-sm leading-6 text-slate-500">
                  {dashboardData
                    ? dashboardData.executive_summary.recommendation
                    : "Awaiting live executive data from the backend."}
                </p>
              </CardContent>
            </Card>
          </div>
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
          <MetricListCard
            title="Profit trend"
            description="Current profitability performance and variance"
            items={profitTrendItems}
            accent="emerald"
          />
          <MetricListCard
            title="Business channel revenue"
            description="Revenue contribution by operating channel"
            items={channelRevenueItems}
            accent="cyan"
          />
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
          <MetricListCard
            title="Monthly channel revenue"
            description="Month-level channel performance summary"
            items={monthlyRevenueItems}
            accent="violet"
          />
          <MetricListCard
            title="Revenue growth"
            description="Growth momentum across core demand signals"
            items={growthItems}
            accent="cyan"
          />
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
          <MetricListCard
            title="Top / lowest performing month"
            description="Peak and trough periods across the year"
            items={monthCards}
            accent="violet"
          />
          <MetricListCard
            title="Best / worst sales day"
            description="Daily performance context for sales planning"
            items={salesDayCards}
            accent="cyan"
          />
        </div>

        <div className="grid gap-6 xl:grid-cols-2">
          <MetricListCard
            title="Revenue by weekday"
            description="Weekly rhythm of demand and spend"
            items={weekdayItems}
            accent="emerald"
          />
          <MetricListCard
            title="Executive health score"
            description="Leadership-readiness signal for the business"
            items={healthScoreItems}
            accent="cyan"
          />
        </div>

        <HeatmapCard
          title="Revenue heatmap"
          description="Weekly and daily intensity pattern across the period"
          rows={heatmapRows}
        />
      </div>
    </DashboardLayout>
  );
}

function dataStatus(data: ExecutiveDashboardResponse) {
  return data.executive_health_score.status;
}
