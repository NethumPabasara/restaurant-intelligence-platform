import pandas as pd


class ExecutiveKPIs:
    """
    Executive KPI calculations.
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

    def _total_revenue(self):
        """Calculate total revenue"""
        return self.sales["Gross Sales"].sum()

    def _total_profit(self):
        """Calculate total estimated profit"""
        return self.sales["Est. Profit"].sum()

    def _total_orders(self):
        """Calculate total unique orders"""
        return self.sales["OrderID"].nunique()

    def _average_daily_orders(self):
        """
        Calculate average daily orders.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        daily_orders = (
            df.groupby("Date")["OrderID"]
            .nunique()
        )

        return daily_orders.mean()

    def _average_order_value(self):
        """Calculate average order value"""

        orders = self._total_orders()

        if orders == 0:
            return 0

        return self._total_revenue() / orders

    def _profit_margin(self):
        """Calculate profit margin percentage"""

        revenue = self._total_revenue()

        if revenue == 0:
            return 0

        return (self._total_profit() / revenue) * 100

    def _revenue_trend(self):
        """
        Calculate monthly revenue trend
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")

        trend = (
            df.groupby("YearMonth")["Gross Sales"]
            .sum()
            .reset_index()
        )

        trend.columns = ["month", "revenue"]

        return trend.to_dict(orient="records")

    def _profit_trend(self):
        """
        Calculate monthly profit trend
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")

        trend = (
            df.groupby("YearMonth")["Est. Profit"]
            .sum()
            .reset_index()
        )

        trend.columns = ["month", "profit"]

        return trend.to_dict(orient="records")

    def get_executive_kpis(self):

        return {

            "cards": {

                "total_revenue": round(self._total_revenue(), 2),

                "total_profit": round(self._total_profit(), 2),

                "total_orders": self._total_orders(),

                "average_order_value": round(
                    self._average_order_value(), 2
                ),

                "profit_margin": round(
                    self._profit_margin(), 2
                )

            },

            "revenue_trend": self._revenue_trend(),

            "profit_trend": self._profit_trend(),

            "business_channel_revenue": self._business_channel_revenue(),

            "monthly_channel_revenue": self._monthly_channel_revenue(),

            "revenue_growth": self._revenue_growth(),

            "top_performing_month": self._top_performing_month(),

            "lowest_performing_month": self._lowest_performing_month(),

            "best_sales_day": self._best_sales_day(),

            "worst_sales_day": self._worst_sales_day(),

            "revenue_by_weekday": self._revenue_by_weekday(),

            "revenue_heatmap": self._revenue_heatmap(),

            "executive_summary": self._executive_summary(),

            "executive_health_score": self._executive_health_score(),

            "ai_business_insights": self._ai_business_insights()

        }

    def _business_channel_revenue(self):
        """
        Calculate revenue by high-level business channels.
        """

        pos_revenue = self.sales["Gross Sales"].sum()

        digital_revenue = self.digital_channels["Revenue"].sum()

        aggregator_revenue = self.aggregator["Revenue"].sum()

        return [

            {
                "channel": "POS",
                "revenue": round(pos_revenue, 2)
            },

            {
                "channel": "Digital",
                "revenue": round(digital_revenue, 2)
            },

            {
                "channel": "Aggregators",
                "revenue": round(aggregator_revenue, 2)
            }

        ]

    def _monthly_channel_revenue(self):
        """
        Calculate monthly revenue by business channel.
        """

        pos = self.sales.copy()

        pos["Date"] = pd.to_datetime(
            pos["Date"],
            format="%d/%m/%Y"
        )

        pos["Month"] = pos["Date"].dt.strftime("%B")

        pos = (
            pos.groupby("Month")["Gross Sales"]
            .sum()
            .reset_index()
        )

        pos.columns = ["Month", "POS"]

        digital = (
            self.digital_channels
            .groupby("Month")["Revenue"]
            .sum()
            .reset_index()
        )

        digital.columns = ["Month", "Digital"]

        aggregator = (
            self.aggregator
            .groupby("Month")["Revenue"]
            .sum()
            .reset_index()
        )

        aggregator.columns = ["Month", "Aggregator"]

        result = (
            pos.merge(digital, on="Month", how="outer")
            .merge(aggregator, on="Month", how="outer")
            .fillna(0)
        )

        return result.to_dict(orient="records")

    def _revenue_growth(self):
        """
        Calculate month-over-month revenue growth (%)
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")

        revenue = (
            df.groupby("YearMonth")["Gross Sales"]
            .sum()
            .reset_index()
        )

        revenue.columns = ["month", "revenue"]

        revenue["growth"] = (
            revenue["revenue"]
            .pct_change() * 100
        )

        revenue["growth"] = (
            revenue["growth"]
            .fillna(0)
            .round(2)
        )

        return revenue.to_dict(orient="records")

    def _top_performing_month(self):
        """
        Find the month with the highest revenue.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")

        revenue = (
            df.groupby("YearMonth")["Gross Sales"]
            .sum()
            .reset_index()
        )

        top_month = revenue.loc[
            revenue["Gross Sales"].idxmax()
        ]

        return {
            "month": top_month["YearMonth"],
            "revenue": round(top_month["Gross Sales"], 2)
        }

    def _lowest_performing_month(self):
        """
        Find the month with the lowest revenue.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")

        revenue = (
            df.groupby("YearMonth")["Gross Sales"]
            .sum()
            .reset_index()
        )

        lowest_month = revenue.loc[
            revenue["Gross Sales"].idxmin()
        ]

        return {
            "month": lowest_month["YearMonth"],
            "revenue": round(lowest_month["Gross Sales"], 2)
        }

    def _best_sales_day(self):
        """
        Find the day with the highest sales.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        daily_sales = (
            df.groupby("Date")["Gross Sales"]
            .sum()
            .reset_index()
        )

        best_day = daily_sales.loc[
            daily_sales["Gross Sales"].idxmax()
        ]

        return {
            "date": best_day["Date"].strftime("%Y-%m-%d"),
            "revenue": round(best_day["Gross Sales"], 2)
        }

    def _worst_sales_day(self):
        """
        Find the day with the lowest sales.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        daily_sales = (
            df.groupby("Date")["Gross Sales"]
            .sum()
            .reset_index()
        )

        worst_day = daily_sales.loc[
            daily_sales["Gross Sales"].idxmin()
        ]

        return {
            "date": worst_day["Date"].strftime("%Y-%m-%d"),
            "revenue": round(worst_day["Gross Sales"], 2)
        }

    def _revenue_by_weekday(self):
        """
        Calculate revenue by weekday.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["Weekday"] = df["Date"].dt.day_name()

        revenue = (
            df.groupby("Weekday")["Gross Sales"]
            .sum()
            .reset_index()
        )

        weekday_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        revenue["Weekday"] = pd.Categorical(
            revenue["Weekday"],
            categories=weekday_order,
            ordered=True
        )

        revenue = revenue.sort_values("Weekday")

        revenue.columns = ["weekday", "revenue"]

        return revenue.to_dict(orient="records")

    def _revenue_heatmap(self):
        """
        Calculate revenue by Month and Weekday.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["Month"] = df["Date"].dt.strftime("%B")
        df["Weekday"] = df["Date"].dt.day_name()

        heatmap = (
            df.groupby(
                ["Month", "Weekday"]
            )["Gross Sales"]
            .sum()
            .reset_index()
        )

        month_order = [
            "January","February","March","April",
            "May","June","July","August",
            "September","October","November","December"
        ]

        weekday_order = [
            "Monday","Tuesday","Wednesday",
            "Thursday","Friday","Saturday","Sunday"
        ]

        heatmap["Month"] = pd.Categorical(
            heatmap["Month"],
            categories=month_order,
            ordered=True
        )

        heatmap["Weekday"] = pd.Categorical(
            heatmap["Weekday"],
            categories=weekday_order,
            ordered=True
        )

        heatmap = heatmap.sort_values(
            ["Month", "Weekday"]
        )

        heatmap.columns = [
            "month",
            "weekday",
            "revenue"
        ]

        return heatmap.to_dict(
            orient="records"
        )

    def _executive_summary(self):
        """
        Generate a rule-based executive summary.
        """

        profit_margin = self._profit_margin()

        revenue_growth = self._revenue_growth()

        top_month = self._top_performing_month()

        lowest_month = self._lowest_performing_month()

        best_day = self._best_sales_day()

        weekday_data = self._revenue_by_weekday()

        latest_growth = revenue_growth[-1]["growth"]

        if profit_margin >= 40 and latest_growth >= 0:
            business_status = "Healthy"

        elif profit_margin >= 25:
            business_status = "Needs Attention"

        else:
            business_status = "Critical"

        strongest_day = max(
            weekday_data,
            key=lambda x: x["revenue"]
        )["weekday"]

        if strongest_day in ["Friday", "Saturday"]:
            recommendation = (
                "Increase staffing and inventory on weekends."
            )
        else:
            recommendation = (
                "Review sales strategy to improve peak-day performance."
            )

        return {

            "business_status": business_status,

            "revenue_summary":
                f"Highest revenue month: {top_month['month']} (£{top_month['revenue']})",

            "profit_summary":
                f"Current profit margin: {round(profit_margin, 2)}%",

            "sales_summary":
                f"Best sales day: {best_day['date']}",

            "risk_summary":
                f"Lowest revenue month: {lowest_month['month']} (£{lowest_month['revenue']})",

            "recommendation":
                recommendation

        }

    def _executive_health_score(self):
        """
        Calculate overall business health score.
        """

        score = 0

        profit_margin = self._profit_margin()

        if profit_margin >= 40:
            score += 30
        elif profit_margin >= 30:
            score += 25
        elif profit_margin >= 20:
            score += 18
        elif profit_margin >= 10:
            score += 10
        else:
            score += 5

        latest_growth = self._revenue_growth()[-1]["growth"]

        if latest_growth >= 10:
            score += 25
        elif latest_growth >= 0:
            score += 20
        elif latest_growth >= -10:
            score += 12
        else:
            score += 5

        status = self._executive_summary()["business_status"]

        if status == "Healthy":
            score += 20
        elif status == "Needs Attention":
            score += 12
        else:
            score += 5

        revenue_data = self._revenue_trend()

        revenues = [
            month["revenue"]
            for month in revenue_data
        ]

        std = pd.Series(revenues).std()

        if std < 200:
            score += 15
        elif std < 500:
            score += 10
        else:
            score += 5

        highest = self._top_performing_month()["revenue"]
        lowest = self._lowest_performing_month()["revenue"]

        ratio = lowest / highest

        if ratio >= 0.75:
            score += 10
        elif ratio >= 0.50:
            score += 7
        else:
            score += 4

        if score >= 90:
            status = "Excellent"
            color = "green"

        elif score >= 75:
            status = "Healthy"
            color = "green"

        elif score >= 60:
            status = "Needs Attention"
            color = "yellow"

        elif score >= 40:
            status = "At Risk"
            color = "orange"

        else:
            status = "Critical"
            color = "red"

        return {

            "score": score,

            "status": status,

            "color": color

        }

    def _ai_business_insights(self):
        """
        Generate AI-like business insights using business rules.
        """

        insights = []

        latest_growth = self._revenue_growth()[-1]["growth"]

        if latest_growth > 10:
            insights.append(
                "Revenue is growing strongly compared to the previous month."
            )

        elif latest_growth >= 0:
            insights.append(
                "Revenue remains stable with positive growth."
            )

        else:
            insights.append(
                "Revenue has declined compared to the previous month."
            )

        profit_margin = self._profit_margin()

        if profit_margin >= 40:
            insights.append(
                "Profit margin is healthy and supports sustainable growth."
            )

        elif profit_margin >= 25:
            insights.append(
                "Profit margin is acceptable but should be monitored."
            )

        else:
            insights.append(
                "Low profit margin detected. Review operating costs."
            )

        weekday_data = self._revenue_by_weekday()

        best_day = max(
            weekday_data,
            key=lambda x: x["revenue"]
        )

        insights.append(
            f"{best_day['weekday']} is currently the strongest sales day."
        )

        lowest = self._lowest_performing_month()

        insights.append(
            f"{lowest['month']} recorded the lowest monthly revenue."
        )

        insights.append(
            "Consider increasing promotions during weaker weekdays to improve overall revenue."
        )

        return insights