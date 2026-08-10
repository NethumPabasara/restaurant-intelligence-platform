import pandas as pd

from .executive_kpis import ExecutiveKPIs


class SalesKPIs(ExecutiveKPIs):
    """
    Sales KPI calculations.
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
    # Sales & Operations
    # =====================================================

    def get_sales_kpis(self):

        return {

            "cards": {

                "total_orders": self._total_orders(),

                "total_sales": round(
                    self._total_revenue(), 2
                ),

                "average_order_value": round(
                    self._average_order_value(), 2
                ),

                "average_daily_orders": round(
                    self._average_daily_orders(), 2
                )

            },

            "orders_trend": self._orders_trend(),

            "sales_trend": self._revenue_trend(),

            "orders_by_hour": self._orders_by_hour(),

            "peak_business_hours": self._peak_business_hours(),

            "quiet_business_hours": self._quiet_business_hours(),

            "revenue_by_weekday": self._revenue_by_weekday(),

            "orders_by_weekday": self._orders_by_weekday(),

            "top_selling_categories": self._top_selling_categories(),

            "top_selling_menu_items": self._top_selling_menu_items(),

            "order_type_distribution": self._order_type_distribution(),

            "payment_method_distribution": self._payment_method_distribution(),

            "cancelled_orders_analysis": self._cancelled_orders_analysis(),

            "ai_sales_insights": self._ai_sales_insights()

        }

    def _orders_trend(self):
        """
        Calculate monthly order trend.
        """

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["YearMonth"] = df["Date"].dt.strftime("%Y-%m")

        trend = (
            df.groupby("YearMonth")["OrderID"]
            .nunique()
            .reset_index()
        )

        trend.columns = ["month", "orders"]

        return trend.to_dict(orient="records")

    def _orders_by_hour(self):
        """
        Calculate orders by hour.
        """

        df = self.sales.copy()

        df["Hour"] = (
           pd.to_datetime(df["Time"], format="%H:%M")
          .dt.hour
        )

        hourly = (
         df.groupby("Hour")["OrderID"]
         .nunique()
            .reset_index()
        )

        hourly.columns = ["hour", "orders"]

        return hourly.to_dict(orient="records")

    def _peak_business_hours(self):
        """
        Get the top 5 busiest hours based on number of orders.
        """

        df = self.sales.copy()

        df["Hour"] = (
            pd.to_datetime(
            df["Time"],
            format="%H:%M"
        ).dt.hour
        )

        peak = (
            df.groupby("Hour")["OrderID"]
            .nunique()
            .reset_index()
            .sort_values(
                by="OrderID",
                ascending=False
            )
            .head(5)
        )

        peak.columns = ["hour", "orders"]

        return peak.to_dict(orient="records")

    def _quiet_business_hours(self):
        """
        Get the 5 quietest business hours based on number of orders.
        """

        df = self.sales.copy()

        df["Hour"] = (
            pd.to_datetime(
                df["Time"],
                format="%H:%M"
            ).dt.hour
        )

        quiet = (
            df.groupby("Hour")["OrderID"]
            .nunique()
            .reset_index()
            .sort_values(
                by="OrderID",
                ascending=True
            )
            .head(5)
        )

        quiet.columns = ["hour", "orders"]

        return quiet.to_dict(orient="records")

    def _orders_by_weekday(self):
        """
        Calculate orders by weekday.
        """

        df = self.sales.copy()

        if "DayOfWeek" in df.columns:
            weekday_values = df["DayOfWeek"]

        elif "Date" in df.columns:
            df["Date"] = pd.to_datetime(
                df["Date"],
                format="%d/%m/%Y"
            )
            weekday_values = df["Date"].dt.day_name()

        else:
            return {
                "available": False,
                "message": "Weekday data is not available in the dataset."
            }

        orders = (
            df.assign(Weekday=weekday_values)
            .groupby("Weekday")["OrderID"]
            .nunique()
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

        orders["Weekday"] = pd.Categorical(
            orders["Weekday"],
            categories=weekday_order,
            ordered=True
        )

        orders = orders.sort_values("Weekday")

        orders.columns = ["weekday", "orders"]

        return orders.to_dict(orient="records")

    def _top_selling_categories(self):
        """
        Calculate top-selling categories by total quantity sold.
        """

        if "Category" not in self.sales.columns:
            return {
                "available": False,
                "message": "Category data is not available in the dataset."
            }

        if "Quantity" not in self.sales.columns:
            return {
                "available": False,
                "message": "Quantity data is not available in the dataset."
            }

        df = self.sales.copy()

        df["Quantity"] = pd.to_numeric(
            df["Quantity"],
            errors="coerce"
        ).fillna(0)

        categories = (
            df.groupby("Category")["Quantity"]
            .sum()
            .reset_index()
            .sort_values(by="Quantity", ascending=False)
        )

        categories.columns = ["category", "quantity"]

        return categories.to_dict(orient="records")

    def _top_selling_menu_items(self):
        """
        Calculate top-selling menu items by total quantity sold.
        """

        item_columns = [
            "Item",
            "Menu",
            "Product",
            "Line item name",
            "Line Item Name",
            "Item Name"
        ]

        item_column = None

        for column in item_columns:
            if column in self.sales.columns:
                item_column = column
                break

        if item_column is None:
            return {
                "available": False,
                "message": "Item-level sales data is not available in the dataset."
            }

        if "Quantity" not in self.sales.columns:
            return {
                "available": False,
                "message": "Quantity data is not available in the dataset."
            }

        df = self.sales.copy()

        df["Quantity"] = pd.to_numeric(
            df["Quantity"],
            errors="coerce"
        ).fillna(0)

        items = (
            df.groupby(item_column)["Quantity"]
            .sum()
            .reset_index()
            .sort_values(by="Quantity", ascending=False)
        )

        items.columns = ["item", "quantity"]

        return items.to_dict(orient="records")

    def _order_type_distribution(self):
        """
        Calculate total orders by order type.
        """

        if "OrderType" not in self.sales.columns:
            return {
                "available": False,
                "message": "Order type data is not available in the dataset."
            }

        order_types = (
            self.sales.groupby("OrderType")
            .size()
            .reset_index(name="orders")
        )

        order_types.columns = ["order_type", "orders"]

        return order_types.to_dict(orient="records")

    def _payment_method_distribution(self):
        """
        Calculate total orders by payment method.
        """

        if "Payment" not in self.sales.columns:
            return {
                "available": False,
                "message": "Payment data is not available in the dataset."
            }

        payments = (
            self.sales.groupby("Payment")
            .size()
            .reset_index(name="orders")
        )

        payments.columns = ["payment_method", "orders"]

        return payments.to_dict(orient="records")

    def _cancelled_orders_analysis(self):
        """
        Calculate cancelled order metrics when available.
        """

        cancelled_columns = [
            "Cancelled",
            "Status",
            "Cancellation Status",
            "Cancelled Flag"
        ]

        cancelled_column = None

        for column in cancelled_columns:
            if column in self.sales.columns:
                cancelled_column = column
                break

        if cancelled_column is None:
            return {
                "available": False,
                "message": "Cancellation data not available in the dataset."
            }

        cancelled_values = self.sales[cancelled_column]

        cancelled_mask = (
            cancelled_values.astype(str)
            .str.strip()
            .str.lower()
            .isin(["yes", "true", "y", "1", "cancelled", "canceled"])
        )

        total_cancelled = int(cancelled_mask.sum())
        total_orders = len(self.sales)

        if total_orders == 0:
            cancellation_rate = 0

        else:
            cancellation_rate = round(
                (total_cancelled / total_orders) * 100,
                2
            )

        return {
            "total_cancelled": total_cancelled,
            "cancellation_rate": cancellation_rate
        }

    def _ai_sales_insights(self):
        """
        Generate rule-based sales insights.
        """

        insights = []

        weekday_data = self._revenue_by_weekday()

        if isinstance(weekday_data, list) and len(weekday_data) > 0:
            best_weekday = max(
                weekday_data,
                key=lambda x: x["revenue"]
            )
            insights.append(
                f"{best_weekday['weekday']} is the strongest weekday for revenue."
            )

        else:
            insights.append(
                "Weekday revenue data is not available in the dataset."
            )

        order_types = self._order_type_distribution()

        if isinstance(order_types, list) and len(order_types) > 0:
            best_order_type = max(
                order_types,
                key=lambda x: x["orders"]
            )
            insights.append(
                f"{best_order_type['order_type']} is the most common order type."
            )

        else:
            insights.append(
                "Order type data is not available in the dataset."
            )

        payments = self._payment_method_distribution()

        if isinstance(payments, list) and len(payments) > 0:
            best_payment = max(
                payments,
                key=lambda x: x["orders"]
            )
            insights.append(
                f"{best_payment['payment_method']} is the most used payment method."
            )

        else:
            insights.append(
                "Payment method data is not available in the dataset."
            )

        categories = self._top_selling_categories()

        if isinstance(categories, list) and len(categories) > 0:
            best_category = max(
                categories,
                key=lambda x: x["quantity"]
            )
            insights.append(
                f"{best_category['category']} is the highest-selling category."
            )

        else:
            insights.append(
                "Category sales data is not available in the dataset."
            )

        if isinstance(weekday_data, list) and len(weekday_data) > 0:
            strongest_weekday = max(
                weekday_data,
                key=lambda x: x["revenue"]
            )["weekday"]

            if strongest_weekday in ["Friday", "Saturday", "Sunday"]:
                recommendation = (
                    "Increase staffing and inventory on peak weekend days."
                )
            else:
                recommendation = (
                    "Review promotions and staffing on quieter weekdays."
                )

        else:
            recommendation = (
                "Review marketing and operations to improve sales performance."
            )

        insights.append(recommendation)

        return insights
