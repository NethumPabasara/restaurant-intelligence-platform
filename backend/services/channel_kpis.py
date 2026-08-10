import pandas as pd

from .executive_kpis import ExecutiveKPIs


class ChannelKPIs(ExecutiveKPIs):
    """
    Channel KPI calculations.
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
    # Channel Intelligence
    # =====================================================

    def get_channel_kpis(self):

        return {

            "cards": {

                "total_channel_revenue": self._total_channel_revenue(),

                "best_channel": self._best_performing_channel(),

                "worst_channel": self._worst_performing_channel(),

                "total_channels": len(self._revenue_by_channel())

            },

            "revenue_by_channel": self._revenue_by_channel(),

            "monthly_channel_revenue": self._monthly_channel_revenue(),

            "channel_share": self._channel_share(),

            "channel_growth": self._channel_growth(),

            "digital_vs_aggregator": self._digital_vs_aggregator(),

            "best_performing_channel": self._best_performing_channel(),

            "worst_performing_channel": self._worst_performing_channel(),

            "ai_channel_insights": self._ai_channel_insights()

        }

    def _total_channel_revenue(self):
        """
        Calculate total revenue by business channel.
        """

        channel_revenue = {}

        if "Gross Sales" in self.sales.columns:
            channel_revenue["POS"] = round(self.sales["Gross Sales"].sum(), 2)

        if "Revenue" in self.digital_channels.columns:
            channel_revenue["Digital"] = round(self.digital_channels["Revenue"].sum(), 2)

        if "Revenue" in self.aggregator.columns:
            channel_revenue["Aggregator"] = round(self.aggregator["Revenue"].sum(), 2)

        return channel_revenue

    def _revenue_by_channel(self):
        """
        Return total revenue grouped by channel.
        """

        revenue_data = []

        channel_revenue = self._total_channel_revenue()

        for channel, revenue in channel_revenue.items():
            revenue_data.append({
                "channel": channel,
                "revenue": revenue
            })

        return revenue_data

    def _monthly_channel_revenue(self):
        """
        Return monthly revenue for each channel.
        """

        result = []

        if "Date" in self.sales.columns and "Gross Sales" in self.sales.columns:
            pos = self.sales.copy()

            pos["Date"] = pd.to_datetime(
                pos["Date"],
                format="%d/%m/%Y"
            )

            pos["Month"] = pos["Date"].dt.strftime("%Y-%m")

            pos_revenue = (
                pos.groupby("Month")["Gross Sales"]
                .sum()
                .reset_index()
            )

            pos_revenue.columns = ["month", "POS"]

            result.append(pos_revenue)

        if "Month" in self.digital_channels.columns and "Revenue" in self.digital_channels.columns:
            digital = self.digital_channels.copy()
            digital.columns = [col.strip() for col in digital.columns]

            if "Month" in digital.columns and "Revenue" in digital.columns:
                digital_revenue = (
                    digital.groupby("Month")["Revenue"]
                    .sum()
                    .reset_index()
                )

                digital_revenue.columns = ["month", "Digital"]

                result.append(digital_revenue)

        if "Month" in self.aggregator.columns and "Revenue" in self.aggregator.columns:
            aggregator = self.aggregator.copy()
            aggregator.columns = [col.strip() for col in aggregator.columns]

            if "Month" in aggregator.columns and "Revenue" in aggregator.columns:
                aggregator_revenue = (
                    aggregator.groupby("Month")["Revenue"]
                    .sum()
                    .reset_index()
                )

                aggregator_revenue.columns = ["month", "Aggregator"]

                result.append(aggregator_revenue)

        if len(result) == 0:
            return []

        merged = result[0]

        for frame in result[1:]:
            merged = merged.merge(frame, on="month", how="outer")

        merged = merged.fillna(0)

        return merged.to_dict(orient="records")

    def _channel_share(self):
        """
        Calculate percentage contribution of each channel.
        """

        revenue_data = self._revenue_by_channel()

        if len(revenue_data) == 0:
            return []

        total_revenue = sum(item["revenue"] for item in revenue_data)

        if total_revenue == 0:
            return []

        contribution = []

        for item in revenue_data:
            contribution.append({
                "channel": item["channel"],
                "revenue": round(item["revenue"], 2),
                "share_pct": round((item["revenue"] / total_revenue) * 100, 2)
            })

        return contribution

    def _best_performing_channel(self):
        """
        Find the channel with the highest revenue.
        """

        revenue_data = self._revenue_by_channel()

        if len(revenue_data) == 0:
            return {
                "channel": None,
                "revenue": 0
            }

        best_channel = max(
            revenue_data,
            key=lambda x: x["revenue"]
        )

        return {
            "channel": best_channel["channel"],
            "revenue": round(best_channel["revenue"], 2)
        }

    def _worst_performing_channel(self):
        """
        Find the channel with the lowest revenue.
        """

        revenue_data = self._revenue_by_channel()

        if len(revenue_data) == 0:
            return {
                "channel": None,
                "revenue": 0
            }

        worst_channel = min(
            revenue_data,
            key=lambda x: x["revenue"]
        )

        return {
            "channel": worst_channel["channel"],
            "revenue": round(worst_channel["revenue"], 2)
        }

    def _channel_growth(self):
        """
        Calculate monthly revenue trend by channel.
        """

        monthly_data = self._monthly_channel_revenue()

        if len(monthly_data) == 0:
            return []

        growth = []

        for item in monthly_data:
            growth.append({
                "month": item["month"],
                "revenue": item.get("POS", 0)
            })

        return growth

    def _digital_vs_aggregator(self):
        """
        Compare digital and aggregator revenue.
        """

        digital = 0
        aggregator = 0

        if "Revenue" in self.digital_channels.columns:
            digital = round(self.digital_channels["Revenue"].sum(), 2)

        if "Revenue" in self.aggregator.columns:
            aggregator = round(self.aggregator["Revenue"].sum(), 2)

        return {
            "digital": digital,
            "aggregator": aggregator,
            "difference": round(digital - aggregator, 2)
        }

    def _ai_channel_insights(self):
        """
        Generate rule-based channel insights.
        """

        insights = []

        revenue_data = self._revenue_by_channel()

        if len(revenue_data) > 0:
            highest = max(revenue_data, key=lambda x: x["revenue"])
            lowest = min(revenue_data, key=lambda x: x["revenue"])
            insights.append(
                f"{highest['channel']} generates the highest revenue."
            )
            insights.append(
                f"{lowest['channel']} generates the lowest revenue."
            )

            largest_share = max(
                self._channel_share(),
                key=lambda x: x["share_pct"]
            ) if len(self._channel_share()) > 0 else None

            if largest_share is not None:
                insights.append(
                    f"{largest_share['channel']} contributes the largest share of revenue."
                )

        else:
            insights.append(
                "Channel revenue data is not available in the dataset."
            )

        digital_vs_aggregator = self._digital_vs_aggregator()

        if digital_vs_aggregator["digital"] >= digital_vs_aggregator["aggregator"]:
            insights.append(
                "Prioritize growth initiatives for digital channels to sustain momentum."
            )
        else:
            insights.append(
                "Increase marketing support for aggregator channels to improve growth."
            )

        insights.append(
            "Review channel performance regularly and adjust promotions to improve revenue mix."
        )

        return insights
