"use client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface OrderTypePoint {
  order_type: string;
  orders: number;
}

interface Props {
  data: OrderTypePoint[];
}

const COLORS = [
  "#06b6d4",
  "#8b5cf6",
  "#10b981",
  "#f59e0b",
];

export function OrderTypeDistributionChart({
  data,
}: Props) {
  return (
    <Card className="border-white/10 bg-white/5 backdrop-blur-xl">

      <CardHeader>
        <CardTitle className="text-white">
          Order Type Distribution
        </CardTitle>
      </CardHeader>

    <CardContent>

  <div className="space-y-8">

    {data.map((item) => {

      const total = data.reduce(
        (sum, x) => sum + x.orders,
        0
      );

      const percentage =
        (item.orders / total) * 100;

      return (

        <div key={item.order_type}>

          <div className="flex justify-between text-white mb-2">

            <span>
              {item.order_type}
            </span>

            <span>
              {item.orders} Orders ({percentage.toFixed(1)}%)
            </span>

          </div>

          <div className="h-4 rounded-full bg-slate-700">

            <div
              className="h-4 rounded-full bg-cyan-500 transition-all duration-700"
              style={{
                width: `${percentage}%`,
              }}
            />

          </div>

        </div>

      );

    })}

  </div>

</CardContent>

    </Card>
  );
}