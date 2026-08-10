import pandas as pd

from .executive_kpis import ExecutiveKPIs


class FinancialKPIs(ExecutiveKPIs):
    """
    Financial KPI calculations.
    """

    def __init__(self, loader):

        self.loader = loader

        self.sales = loader.sales
        self.digital_channels = loader.digital_channels
        self.aggregator = loader.aggregator
        self.deliveroo = loader.deliveroo
        self.epos_summary = loader.epos_summary
        self.epos_mix = loader.epos_mix
        self.pnl = loader.pnl

    # =====================================================
    # Financial Analytics
    # =====================================================

    def get_financial_kpis(self):

        return {

            "cards": {

                "total_revenue": self._total_revenue(),

                "total_profit": self._total_profit(),

                "total_expenses": self._total_expenses(),

                "profit_margin": self._profit_margin(),

                "net_profit": self._net_profit()

            },

            "monthly_revenue_trend": self._monthly_revenue_trend(),

            "monthly_profit_trend": self._monthly_profit_trend(),

            "monthly_expense_trend": self._monthly_expense_trend(),

            "revenue_vs_profit": self._revenue_vs_profit(),

            "revenue_growth": self._revenue_growth(),

            "profit_growth": self._profit_growth(),

            "expense_breakdown": self._expense_breakdown(),

            "highest_expense_category": self._highest_expense_category(),

            "lowest_expense_category": self._lowest_expense_category(),

            "financial_health_score": self._financial_health_score(),

            "financial_summary": self._financial_summary(),

            "ai_financial_insights": self._ai_financial_insights()

        }

    def _total_revenue(self):
        """
        Calculate total revenue.
        """

        return round(self.sales["Gross Sales"].sum(), 2)

    def _total_profit(self):
        """
        Calculate total profit.
        """

        return round(self.sales["Est. Profit"].sum(), 2)

    def _total_expenses(self):
        """
        Calculate total expenses.
        """

        if "Est. Cost" in self.sales.columns:
            return round(self.sales["Est. Cost"].sum(), 2)

        if self.pnl is not None and not self.pnl.empty:
            expense_columns = [
                col for col in self.pnl.columns
                if col.lower() != "month"
            ]

            if len(expense_columns) > 0:
                return round(self.pnl[expense_columns].sum().sum(), 2)

        return 0

    def _profit_margin(self):
        """
        Calculate profit margin percentage.
        """

        revenue = self._total_revenue()

        if revenue == 0:
            return 0

        return round((self._total_profit() / revenue) * 100, 2)

    def _net_profit(self):
        """
        Calculate net profit.
        """

        return round(self._total_profit() - self._total_expenses(), 2)

    def _monthly_revenue_trend(self):
        """
        Calculate monthly revenue trend.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        revenue = (
            df.groupby("Month")["Gross Sales"]
            .sum()
            .reset_index()
        )

        revenue.columns = ["month", "revenue"]

        return revenue.to_dict(orient="records")

    def _monthly_profit_trend(self):
        """
        Calculate monthly profit trend.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        profit = (
            df.groupby("Month")["Est. Profit"]
            .sum()
            .reset_index()
        )

        profit.columns = ["month", "profit"]

        return profit.to_dict(orient="records")

    def _monthly_expense_trend(self):
        """
        Calculate monthly expense trend.
        """

        if self.pnl is None or self.pnl.empty:
            return {
                "available": False,
                "message": "Monthly expense data is not available in the dataset."
            }

        df = self.pnl.copy()

        df.columns = [col.strip() for col in df.columns]

        if "Month" not in df.columns:
            return {
                "available": False,
                "message": "Monthly expense data is not available in the dataset."
            }

        expense_columns = [
            col for col in df.columns
            if col.lower() != "month"
        ]

        if len(expense_columns) == 0:
            return {
                "available": False,
                "message": "Monthly expense data is not available in the dataset."
            }

        expense_data = []

        for _, row in df.iterrows():
            month = row["Month"]
            total_expenses = 0

            for column in expense_columns:
                value = row[column]

                if pd.notna(value):
                    total_expenses += float(value)

            expense_data.append({
                "month": month,
                "expenses": round(total_expenses, 2)
            })

        return expense_data

    def _revenue_vs_profit(self):
        """
        Compare monthly revenue and profit.
        """

        revenue_trend = self._monthly_revenue_trend()
        profit_trend = self._monthly_profit_trend()

        comparison = []

        for item in revenue_trend:
            month = item["month"]
            profit_item = next(
                (entry for entry in profit_trend if entry["month"] == month),
                None
            )

            comparison.append({
                "month": month,
                "revenue": round(item["revenue"], 2),
                "profit": round(profit_item["profit"], 2) if profit_item else 0
            })

        return comparison

    def _revenue_growth(self):
        """
        Calculate month-over-month revenue growth percentage.
        """

        revenue_trend = self._monthly_revenue_trend()

        if len(revenue_trend) == 0:
            return []

        growth = []

        for index, item in enumerate(revenue_trend):
            if index == 0:
                growth.append({
                    "month": item["month"],
                    "growth": 0
                })
            else:
                previous = revenue_trend[index - 1]["revenue"]
                current = item["revenue"]

                if previous == 0:
                    growth_value = 0
                else:
                    growth_value = round(((current - previous) / previous) * 100, 2)

                growth.append({
                    "month": item["month"],
                    "growth": growth_value
                })

        return growth

    def _profit_growth(self):
        """
        Calculate month-over-month profit growth percentage.
        """

        profit_trend = self._monthly_profit_trend()

        if len(profit_trend) == 0:
            return []

        growth = []

        for index, item in enumerate(profit_trend):
            if index == 0:
                growth.append({
                    "month": item["month"],
                    "growth": 0
                })
            else:
                previous = profit_trend[index - 1]["profit"]
                current = item["profit"]

                if previous == 0:
                    growth_value = 0
                else:
                    growth_value = round(((current - previous) / previous) * 100, 2)

                growth.append({
                    "month": item["month"],
                    "growth": growth_value
                })

        return growth

    def _expense_breakdown(self):
        """
        Calculate expense breakdown from PnL data.
        """

        if self.pnl is None or self.pnl.empty:
            return {
                "available": False,
                "message": "Expense data is not available in the dataset."
            }

        df = self.pnl.copy()
        df.columns = [col.strip() for col in df.columns]

        if "Month" not in df.columns:
            return {
                "available": False,
                "message": "Expense data is not available in the dataset."
            }

        expense_columns = [
            col for col in df.columns
            if col.lower() != "month"
        ]

        if len(expense_columns) == 0:
            return {
                "available": False,
                "message": "Expense data is not available in the dataset."
            }

        latest_row = df.iloc[-1]
        expenses = []

        for column in expense_columns:
            value = latest_row[column]

            if pd.notna(value):
                expenses.append({
                    "category": column,
                    "amount": round(float(value), 2)
                })

        return expenses

    def _highest_expense_category(self):
        """
        Find the highest expense category.
        """

        expense_data = self._expense_breakdown()

        if isinstance(expense_data, dict):
            return expense_data

        if len(expense_data) == 0:
            return {
                "category": None,
                "amount": 0
            }

        highest = max(expense_data, key=lambda x: x["amount"])

        return {
            "category": highest["category"],
            "amount": round(highest["amount"], 2)
        }

    def _lowest_expense_category(self):
        """
        Find the lowest expense category.
        """

        expense_data = self._expense_breakdown()

        if isinstance(expense_data, dict):
            return expense_data

        if len(expense_data) == 0:
            return {
                "category": None,
                "amount": 0
            }

        lowest = min(expense_data, key=lambda x: x["amount"])

        return {
            "category": lowest["category"],
            "amount": round(lowest["amount"], 2)
        }

    def _financial_health_score(self):
        """
        Calculate financial health score.
        """

        profit_margin = self._profit_margin()
        revenue_growth = self._revenue_growth()
        expense_breakdown = self._expense_breakdown()

        latest_growth = 0

        if isinstance(revenue_growth, list) and len(revenue_growth) > 0:
            latest_growth = revenue_growth[-1]["growth"]

        expense_ratio = 0

        if isinstance(expense_breakdown, list) and len(expense_breakdown) > 0:
            total_expenses = sum(item["amount"] for item in expense_breakdown)
            total_revenue = self._total_revenue()

            if total_revenue != 0:
                expense_ratio = round((total_expenses / total_revenue) * 100, 2)

        score = 0

        if profit_margin >= 20:
            score += 35
        elif profit_margin >= 10:
            score += 25
        elif profit_margin >= 0:
            score += 15
        else:
            score += 5

        if latest_growth >= 10:
            score += 35
        elif latest_growth >= 0:
            score += 20
        elif latest_growth >= -10:
            score += 10
        else:
            score += 5

        if expense_ratio <= 40:
            score += 20
        elif expense_ratio <= 60:
            score += 12
        else:
            score += 5

        if score >= 80:
            status = "Healthy"
            color = "green"
        elif score >= 60:
            status = "Needs Attention"
            color = "yellow"
        else:
            status = "Critical"
            color = "red"

        return {
            "score": score,
            "status": status,
            "color": color
        }

    def _financial_summary(self):
        """
        Generate a rule-based financial summary.
        """

        profit_margin = self._profit_margin()
        revenue_growth = self._revenue_growth()
        latest_growth = 0

        if isinstance(revenue_growth, list) and len(revenue_growth) > 0:
            latest_growth = revenue_growth[-1]["growth"]

        if profit_margin >= 20 and latest_growth >= 0:
            business_status = "Healthy"
        elif profit_margin >= 10:
            business_status = "Needs Attention"
        else:
            business_status = "Critical"

        highest_expense = self._highest_expense_category()
        lowest_expense = self._lowest_expense_category()

        highest_category = highest_expense.get("category") if isinstance(highest_expense, dict) else None
        lowest_category = lowest_expense.get("category") if isinstance(lowest_expense, dict) else None

        return {
            "business_status": business_status,
            "revenue_summary": f"Total revenue: £{round(self._total_revenue(), 2)}",
            "profit_summary": f"Total profit: £{round(self._total_profit(), 2)}",
            "expense_summary": f"Largest expense category: {highest_category}",
            "risk_summary": f"Lowest expense category: {lowest_category}",
            "recommendation": "Review operating costs and increase focus on high-margin revenue streams."
        }

    def _ai_financial_insights(self):
        """
        Generate rule-based financial insights.
        """

        insights = []

        revenue_growth = self._revenue_growth()
        latest_growth = 0

        if isinstance(revenue_growth, list) and len(revenue_growth) > 0:
            latest_growth = revenue_growth[-1]["growth"]

        if latest_growth > 0:
            insights.append("Revenue is increasing.")
        else:
            insights.append("Revenue is not increasing.")

        profit_margin = self._profit_margin()

        if profit_margin >= 20:
            insights.append("Profit margin is healthy.")
        elif profit_margin >= 10:
            insights.append("Profit margin is acceptable.")
        else:
            insights.append("Profit margin is under pressure.")

        highest_expense = self._highest_expense_category()

        if isinstance(highest_expense, dict) and highest_expense.get("category") is not None:
            insights.append(
                f"Largest expense category is {highest_expense['category']}."
            )

        insights.append("Control operating costs.")
        insights.append("Increase high-margin products.")
        insights.append("Review underperforming months.")

        return insights
