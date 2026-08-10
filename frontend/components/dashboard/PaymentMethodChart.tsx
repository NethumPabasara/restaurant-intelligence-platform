"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface PaymentMethod {
  payment_method: string;
  orders: number;
}

interface Props {
  data: PaymentMethod[];
}

export function PaymentMethodChart({
  data,
}: Props) {

  const total = data.reduce(
    (sum, item) => sum + item.orders,
    0
  );

  return (

    <Card className="border-white/10 bg-white/5 backdrop-blur-xl">

      <CardHeader>
        <CardTitle className="text-white">
          Payment Method Distribution
        </CardTitle>
      </CardHeader>

      <CardContent>

        <div className="space-y-6">

          {data.map((item) => {

            const percentage =
              (item.orders / total) * 100;

            return (

              <div key={item.payment_method}>

                <div className="flex justify-between text-white mb-2">

                  <span>
                    💳 {item.payment_method}
                  </span>

                  <span>
                    {item.orders} ({percentage.toFixed(1)}%)
                  </span>

                </div>

                <div className="h-4 rounded-full bg-slate-700">

                  <div
                    className="h-4 rounded-full bg-violet-500 transition-all duration-700"
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