import pandas as pd

from .executive_kpis import ExecutiveKPIs


class ProductKPIs(ExecutiveKPIs):
    """
    Product KPI calculations.
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
    # Product Intelligence
    # =====================================================

    def get_product_kpis(self):

        return {

            "cards": {

                "total_products_sold": self._total_products_sold(),

                "total_categories": self._total_categories(),

                "average_items_per_order": self._average_items_per_order(),

                "average_revenue_per_product": self._average_revenue_per_product()

            },

            "top_selling_categories": self._top_selling_categories(),

            "worst_selling_categories": self._worst_selling_categories(),

            "revenue_by_category": self._revenue_by_category(),

            "quantity_by_category": self._quantity_by_category(),

            "category_contribution": self._category_contribution(),

            "monthly_category_revenue": self._monthly_category_revenue(),

            "best_performing_category": self._best_performing_category(),

            "worst_performing_category": self._worst_performing_category(),

            "fast_moving_categories": self._fast_moving_categories(),

            "slow_moving_categories": self._slow_moving_categories(),

            "ai_product_insights": self._ai_product_insights()

        }

    def _total_products_sold(self):
        """
        Calculate total quantity sold.
        """

        if "Quantity" not in self.sales.columns:
            return 0

        return int(self.sales["Quantity"].sum())

    def _total_categories(self):
        """
        Calculate total unique categories.
        """

        if "Category" not in self.sales.columns:
            return 0

        return self.sales["Category"].nunique()

    def _average_items_per_order(self):
        """
        Calculate average items per order.
        """

        total_orders = self._total_orders()
        total_quantity = self._total_products_sold()

        if total_orders == 0:
            return 0

        return round(total_quantity / total_orders, 2)

    def _average_revenue_per_product(self):
        """
        Calculate average revenue per product.
        """

        total_quantity = self._total_products_sold()

        if total_quantity == 0:
            return 0

        return round(self._total_revenue() / total_quantity, 2)

    def _top_selling_categories(self):
        """
        Get the top 10 categories by quantity sold.
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

        top_categories = (
            df.groupby("Category")["Quantity"]
            .sum()
            .reset_index()
            .sort_values(by="Quantity", ascending=False)
            .head(10)
        )

        top_categories.columns = ["category", "quantity"]

        return top_categories.to_dict(orient="records")

    def _worst_selling_categories(self):
        """
        Get the bottom 10 categories by quantity sold.
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

        worst_categories = (
            df.groupby("Category")["Quantity"]
            .sum()
            .reset_index()
            .sort_values(by="Quantity", ascending=True)
            .head(10)
        )

        worst_categories.columns = ["category", "quantity"]

        return worst_categories.to_dict(orient="records")

    def _revenue_by_category(self):
        """
        Calculate revenue by category.
        """

        if "Category" not in self.sales.columns:
            return {
                "available": False,
                "message": "Category data is not available in the dataset."
            }

        if "Gross Sales" not in self.sales.columns:
            return {
                "available": False,
                "message": "Gross sales data is not available in the dataset."
            }

        revenue = (
            self.sales.groupby("Category")["Gross Sales"]
            .sum()
            .reset_index()
        )

        revenue.columns = ["category", "revenue"]

        return revenue.to_dict(orient="records")

    def _quantity_by_category(self):
        """
        Calculate quantity by category.
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

        quantity = (
            df.groupby("Category")["Quantity"]
            .sum()
            .reset_index()
        )

        quantity.columns = ["category", "quantity"]

        return quantity.to_dict(orient="records")

    def _category_contribution(self):
        """
        Calculate category contribution percentage.
        """

        revenue_data = self._revenue_by_category()

        if isinstance(revenue_data, dict):
            return revenue_data

        if len(revenue_data) == 0:
            return []

        total_revenue = sum(item["revenue"] for item in revenue_data)

        if total_revenue == 0:
            return []

        contribution = []

        for item in revenue_data:
            contribution.append({
                "category": item["category"],
                "revenue": round(item["revenue"], 2),
                "contribution_pct": round(
                    (item["revenue"] / total_revenue) * 100,
                    2
                )
            })

        return contribution

    def _monthly_category_revenue(self):
        """
        Calculate monthly revenue grouped by category.
        """

        if "Category" not in self.sales.columns:
            return {
                "available": False,
                "message": "Category data is not available in the dataset."
            }

        if "Gross Sales" not in self.sales.columns:
            return {
                "available": False,
                "message": "Gross sales data is not available in the dataset."
            }

        if "Date" not in self.sales.columns:
            return {
                "available": False,
                "message": "Date data is not available in the dataset."
            }

        df = self.sales.copy()

        df["Date"] = pd.to_datetime(
            df["Date"],
            format="%d/%m/%Y"
        )

        df["Month"] = df["Date"].dt.strftime("%Y-%m")

        monthly_revenue = (
            df.groupby(["Month", "Category"])["Gross Sales"]
            .sum()
            .reset_index()
        )

        monthly_revenue.columns = ["month", "category", "revenue"]

        return monthly_revenue.to_dict(orient="records")

    def _best_performing_category(self):
        """
        Find the category with the highest revenue.
        """

        revenue_data = self._revenue_by_category()

        if isinstance(revenue_data, dict):
            return revenue_data

        if len(revenue_data) == 0:
            return {
                "category": None,
                "revenue": 0
            }

        best_category = max(
            revenue_data,
            key=lambda x: x["revenue"]
        )

        return {
            "category": best_category["category"],
            "revenue": round(best_category["revenue"], 2)
        }

    def _worst_performing_category(self):
        """
        Find the category with the lowest revenue.
        """

        revenue_data = self._revenue_by_category()

        if isinstance(revenue_data, dict):
            return revenue_data

        if len(revenue_data) == 0:
            return {
                "category": None,
                "revenue": 0
            }

        worst_category = min(
            revenue_data,
            key=lambda x: x["revenue"]
        )

        return {
            "category": worst_category["category"],
            "revenue": round(worst_category["revenue"], 2)
        }

    def _fast_moving_categories(self):
        """
        Get the categories with the highest quantity sold.
        """

        quantity_data = self._quantity_by_category()

        if isinstance(quantity_data, dict):
            return quantity_data

        if len(quantity_data) == 0:
            return []

        fast_moving = sorted(
            quantity_data,
            key=lambda x: x["quantity"],
            reverse=True
        )

        return fast_moving

    def _slow_moving_categories(self):
        """
        Get the categories with the lowest quantity sold.
        """

        quantity_data = self._quantity_by_category()

        if isinstance(quantity_data, dict):
            return quantity_data

        if len(quantity_data) == 0:
            return []

        slow_moving = sorted(
            quantity_data,
            key=lambda x: x["quantity"]
        )

        return slow_moving

    def _ai_product_insights(self):
        """
        Generate rule-based product insights.
        """

        insights = []

        revenue_data = self._revenue_by_category()

        if isinstance(revenue_data, list) and len(revenue_data) > 0:
            best_revenue = max(
                revenue_data,
                key=lambda x: x["revenue"]
            )
            insights.append(
                f"{best_revenue['category']} generates the highest revenue."
            )

        else:
            insights.append(
                "Revenue by category data is not available in the dataset."
            )

        quantity_data = self._quantity_by_category()

        if isinstance(quantity_data, list) and len(quantity_data) > 0:
            best_quantity = max(
                quantity_data,
                key=lambda x: x["quantity"]
            )
            insights.append(
                f"{best_quantity['category']} has the highest quantity sold."
            )

        else:
            insights.append(
                "Quantity by category data is not available in the dataset."
            )

        if isinstance(revenue_data, list) and len(revenue_data) > 0:
            worst_revenue = min(
                revenue_data,
                key=lambda x: x["revenue"]
            )
            insights.append(
                f"{worst_revenue['category']} is the weakest category by revenue."
            )

        else:
            insights.append(
                "No weak category could be identified."
            )

        insights.append(
            "Review inventory levels for low-volume categories and consider adjusting menu mix."
        )

        insights.append(
            "Prioritize promotional support for high-revenue categories to improve sales performance."
        )

        return insights
