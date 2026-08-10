"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "@/components/layout/DashboardLayout";
import { fetchSalesDashboard } from "@/lib/api";
import { OrdersTrendChart } from "@/components/dashboard/OrdersTrendChart";
import { SalesTrendChart } from "@/components/dashboard/SalesTrendChart";
import { OrdersByHourChart } from "@/components/dashboard/OrdersByHourChart";
import { RevenueByWeekdayChart } from "@/components/dashboard/RevenueByWeekdayChart";
import { OrdersByWeekdayChart } from "@/components/dashboard/OrdersByWeekdayChart";
import { TopSellingCategoriesChart } from "@/components/dashboard/TopSellingCategoriesChart";
import { TopSellingMenuItemsChart } from "@/components/dashboard/TopSellingMenuItemsChart";
import { OrderTypeDistributionChart } from "@/components/dashboard/OrderTypeDistributionChart";
import { PaymentMethodChart } from "@/components/dashboard/PaymentMethodChart";
import {
  DollarSign,
  ShoppingCart,
  Wallet,
  CalendarDays,
  TrendingUp,
} from "lucide-react";

interface SalesDashboardResponse {
  cards: {
    total_orders: number;
    total_sales: number;
    average_order_value: number;
    average_daily_orders: number;
  };

  orders_trend: {
    month: string;
    orders: number;
  }[];

  sales_trend: {
    month: string;
    revenue: number;
  }[];

  orders_by_hour: {
    hour: number;
    orders: number;
  }[];

  peak_business_hours: {
    hour: number;
    orders: number;
  }[];

  quiet_business_hours: {
    hour: number;
    orders: number;
  }[];

  revenue_by_weekday: {
    weekday: string;
    revenue: number;
  }[];

  orders_by_weekday: {
    weekday: string;
    orders: number;
  }[];

  top_selling_categories: {
    category: string;
    quantity: number;
  }[];

  top_selling_menu_items: {
    item: string;
    quantity: number;
  }[];

  order_type_distribution: {
    order_type: string;
    orders: number;
  }[];

  payment_method_distribution: {
    payment_method: string;
    orders: number;
  }[];

  cancelled_orders_analysis: {
    total_cancelled: number;
    cancellation_rate: number;
  };

  ai_sales_insights: string[];
}

export default function SalesPage() {
  const [data, setData] =
  useState<SalesDashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const result = await fetchSalesDashboard();
        setData(result);
      } catch (err) {
        console.error(err);
        setError("Failed to load Sales Dashboard");
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
  <DashboardLayout>
    <div className="space-y-8">

      <div className="flex items-center gap-2 text-sm text-cyan-300">
        📊
        <span>Sales command center</span>
      </div>

      <div>
        <h1 className="text-3xl font-semibold text-white">
          Sales Performance Dashboard
        </h1>

        <p className="mt-2 text-sm text-slate-400">
          Live sales intelligence powered directly from your Restaurant KPI Engine.
        </p>
      </div>

      {loading && (
        <p className="text-white">Loading...</p>
      )}

      {error && (
        <p className="text-red-500">{error}</p>
      )}

      {data && (
        <div className="space-y-8">

          {/* KPI Cards */}
          <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">

            <div className="rounded-2xl border border-emerald-500/20 bg-white/5 p-6 backdrop-blur-xl transition-all duration-300 hover:border-emerald-400 hover:shadow-lg hover:shadow-emerald-500/10">

  <div className="flex items-center justify-between">

    <div className="flex items-center gap-3">

      <div className="rounded-xl bg-emerald-500/15 p-3">
        <DollarSign className="h-6 w-6 text-emerald-400" />
      </div>

      <div>
        <p className="text-sm text-slate-400">
          Total Sales
        </p>

        <p className="text-xs text-emerald-400">
          Revenue Generated
        </p>
      </div>

    </div>

    <TrendingUp className="h-5 w-5 text-emerald-400" />

  </div>

  <div className="mt-6 text-4xl font-bold text-white">
    ${data.cards.total_sales.toFixed(2)}
  </div>

</div>

            <div className="rounded-2xl border border-cyan-500/20 bg-white/5 p-6 backdrop-blur-xl transition-all duration-300 hover:border-cyan-400 hover:shadow-lg hover:shadow-cyan-500/10">

  <div className="flex items-center justify-between">

    <div className="flex items-center gap-3">

      <div className="rounded-xl bg-cyan-500/15 p-3">
        <ShoppingCart className="h-6 w-6 text-cyan-400" />
      </div>

      <div>
        <p className="text-sm text-slate-400">
          Total Orders
        </p>

        <p className="text-xs text-cyan-400">
          Customer Orders
        </p>
      </div>

    </div>

    <TrendingUp className="h-5 w-5 text-cyan-400" />

  </div>

  <div className="mt-6 text-4xl font-bold text-white">
    {data.cards.total_orders}
  </div>

</div>

            <div className="rounded-2xl border border-violet-500/20 bg-white/5 p-6 backdrop-blur-xl transition-all duration-300 hover:border-violet-400 hover:shadow-lg hover:shadow-violet-500/10">

  <div className="flex items-center justify-between">

    <div className="flex items-center gap-3">

      <div className="rounded-xl bg-violet-500/15 p-3">
        <Wallet className="h-6 w-6 text-violet-400" />
      </div>

      <div>
        <p className="text-sm text-slate-400">
          Average Order Value
        </p>

        <p className="text-xs text-violet-400">
          Per Transaction
        </p>
      </div>

    </div>

    <TrendingUp className="h-5 w-5 text-violet-400" />

  </div>

  <div className="mt-6 text-4xl font-bold text-white">
    ${data.cards.average_order_value.toFixed(2)}
  </div>

</div>

            <div className="rounded-2xl border border-orange-500/20 bg-white/5 p-6 backdrop-blur-xl transition-all duration-300 hover:border-orange-400 hover:shadow-lg hover:shadow-orange-500/10">

  <div className="flex items-center justify-between">

    <div className="flex items-center gap-3">

      <div className="rounded-xl bg-orange-500/15 p-3">
        <CalendarDays className="h-6 w-6 text-orange-400" />
      </div>

      <div>
        <p className="text-sm text-slate-400">
          Average Daily Orders
        </p>

        <p className="text-xs text-orange-400">
          Daily Activity
        </p>
      </div>

    </div>

    <TrendingUp className="h-5 w-5 text-orange-400" />

  </div>

  <div className="mt-6 text-4xl font-bold text-white">
    {data.cards.average_daily_orders.toFixed(2)}
  </div>

</div>

          </div>

          {/* Charts */}

          <div className="mt-12 mb-6">
  <h2 className="text-2xl font-bold text-white">
    📈 Sales Trends
  </h2>

  <p className="text-slate-400">
    Revenue growth and sales performance over time.
  </p>
</div>

          <div className="grid gap-6 xl:grid-cols-2">

            

            <OrdersTrendChart
              data={data.orders_trend}
            />

            <SalesTrendChart
              data={data.sales_trend}
            />

          </div>

          <div className="mt-14 mb-6">
  <h2 className="text-2xl font-bold text-white">
    ⏰ Time Analytics
  </h2>

  <p className="text-slate-400">
    Customer ordering behaviour throughout the day and week.
  </p>
</div>

          <div className="mt-8">
            <OrdersByHourChart
            data={data.orders_by_hour}
             />
        </div>

        <div className="mt-8">
            <RevenueByWeekdayChart
            data={data.revenue_by_weekday}
            />
        </div>

        <div className="mt-8">
            <OrdersByWeekdayChart
            data={data.orders_by_weekday}
            />
        </div>

        <div className="mt-14 mb-6">
  <h2 className="text-2xl font-bold text-white">
    🍽 Product Performance
  </h2>

  <p className="text-slate-400">
    Best-selling categories and menu items.
  </p>
</div>

        <div className="mt-8">
            <TopSellingCategoriesChart
            data={data.top_selling_categories}
        />
        </div>

        <div className="mt-8">
            <TopSellingMenuItemsChart
            data={data.top_selling_menu_items}
            />
        </div>

        <div className="mt-14 mb-6">
  <h2 className="text-2xl font-bold text-white">
    👥 Customer Behaviour
  </h2>

  <p className="text-slate-400">
    Order preferences and payment behaviour.
  </p>
</div>

        <div className="mt-8">
            <OrderTypeDistributionChart
            data={data.order_type_distribution}
            />
        </div>

        <div className="mt-8">
            <PaymentMethodChart
            data={data.payment_method_distribution}
            />
        </div>

        <div className="mt-14 mb-6">
  <h2 className="text-2xl font-bold text-white">
    ⚠ Operational Health
  </h2>

  <p className="text-slate-400">
    Cancellation analysis and operational monitoring.
  </p>
</div>

        <div className="rounded-2xl border border-red-500/20 bg-red-500/5 p-6">

  <h2 className="text-xl font-semibold text-white">
    ❌ Cancelled Orders Analysis
  </h2>

  <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">

    <div>
      <p className="text-sm text-slate-400">
        Total Cancelled Orders
      </p>

      <p className="mt-2 text-5xl font-bold text-red-400">
        {data.cancelled_orders_analysis.total_cancelled}
      </p>
    </div>

    <div>
      <p className="text-sm text-slate-400">
        Cancellation Rate
      </p>

      <p className="mt-2 text-5xl font-bold text-orange-400">
        {data.cancelled_orders_analysis.cancellation_rate.toFixed(2)}%
      </p>
    </div>

  </div>

</div>

<div className="mt-14 mb-6">
  <h2 className="text-2xl font-bold text-white">
    🤖 AI Recommendations
  </h2>

  <p className="text-slate-400">
    Business recommendations generated automatically from Restaurant AI.
  </p>
</div>

        <div className="mt-8 rounded-xl border border-white/10 bg-white/5 p-4">

  <p className="text-sm text-slate-400">
    AI Status
  </p>

  <p className="mt-2 text-lg font-semibold">

    {data.cancelled_orders_analysis.cancellation_rate < 5
      ? "🟢 Healthy cancellation rate."
      : data.cancelled_orders_analysis.cancellation_rate < 10
      ? "🟡 Moderate cancellation rate."
      : "🔴 High cancellation rate. Immediate investigation recommended."}

  </p>

</div>

<div className="rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-6">

  <h2 className="text-2xl font-bold text-white">
    🤖 AI Sales Insights
  </h2>

  <p className="mt-2 text-sm text-slate-400">
    Automatically generated business recommendations from Restaurant AI.
  </p>

  <div className="mt-6 space-y-4">

    {data.ai_sales_insights.map((insight, index) => (

      <div
        key={index}
        className="rounded-xl border border-white/10 bg-white/5 p-4"
      >
        <div className="flex items-start gap-3">

          <div className="text-cyan-400 text-xl">
            💡
          </div>

          <p className="text-slate-200">
            {insight}
          </p>

        </div>
      </div>

    ))}

  </div>

</div>

        </div>
      )}

    </div>
  </DashboardLayout>
);
}