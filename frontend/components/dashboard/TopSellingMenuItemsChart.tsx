"use client";

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface MenuItemPoint {
  item: string;
  quantity: number;
}

interface TopSellingMenuItemsChartProps {
  data: MenuItemPoint[];
}

export function TopSellingMenuItemsChart({
  data,
}: TopSellingMenuItemsChartProps) {
  return (
    <Card className="border-white/10 bg-white/5 backdrop-blur-xl">
      <CardHeader>
        <CardTitle className="text-white">
          Top Selling Menu Items
        </CardTitle>
      </CardHeader>

      <CardContent>
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              layout="vertical"
              data={data.slice(0, 10)}
              margin={{
                left: 60,
                right: 20,
              }}
            >
              <CartesianGrid
                stroke="#334155"
                strokeDasharray="3 3"
              />

              <XAxis
                type="number"
                stroke="#94a3b8"
              />

              <YAxis
                dataKey="item"
                type="category"
                stroke="#94a3b8"
                width={170}
              />

              <Tooltip />

              <Bar
                dataKey="quantity"
                fill="#06b6d4"
                radius={[0, 8, 8, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}