try:
    from services.executive_kpis import ExecutiveKPIs
    from services.sales_kpis import SalesKPIs
    from services.product_kpis import ProductKPIs
    from services.channel_kpis import ChannelKPIs
    from services.financial_kpis import FinancialKPIs
except ModuleNotFoundError:
    from backend.services.executive_kpis import ExecutiveKPIs
    from backend.services.sales_kpis import SalesKPIs
    from backend.services.product_kpis import ProductKPIs
    from backend.services.channel_kpis import ChannelKPIs
    from backend.services.financial_kpis import FinancialKPIs


class KPIEngine:
    """
    Restaurant Intelligence KPI Engine.

    This wrapper delegates the dashboard-specific KPI work to dedicated
    service classes for executive, sales, product, channel, and financial
    analytics while preserving the public API used by the FastAPI routes.
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

        self.executive_kpis = ExecutiveKPIs(loader)
        self.sales_kpis = SalesKPIs(loader)
        self.product_kpis = ProductKPIs(loader)
        self.channel_kpis = ChannelKPIs(loader)
        self.financial_kpis = FinancialKPIs(loader)

    def get_executive_kpis(self):
        return self.executive_kpis.get_executive_kpis()

    def _total_revenue(self):
        return self.executive_kpis._total_revenue()

    def _total_profit(self):
        return self.executive_kpis._total_profit()

    def _total_orders(self):
        return self.executive_kpis._total_orders()

    def _average_daily_orders(self):
        return self.executive_kpis._average_daily_orders()

    def _average_order_value(self):
        return self.executive_kpis._average_order_value()

    def _profit_margin(self):
        return self.executive_kpis._profit_margin()

    def _revenue_trend(self):
        return self.executive_kpis._revenue_trend()

    def _profit_trend(self):
        return self.executive_kpis._profit_trend()

    def _business_channel_revenue(self):
        return self.executive_kpis._business_channel_revenue()

    def _monthly_channel_revenue(self):
        return self.executive_kpis._monthly_channel_revenue()

    def _revenue_growth(self):
        return self.executive_kpis._revenue_growth()

    def _top_performing_month(self):
        return self.executive_kpis._top_performing_month()

    def _lowest_performing_month(self):
        return self.executive_kpis._lowest_performing_month()

    def _best_sales_day(self):
        return self.executive_kpis._best_sales_day()

    def _worst_sales_day(self):
        return self.executive_kpis._worst_sales_day()

    def _revenue_by_weekday(self):
        return self.executive_kpis._revenue_by_weekday()

    def _revenue_heatmap(self):
        return self.executive_kpis._revenue_heatmap()

    def _executive_summary(self):
        return self.executive_kpis._executive_summary()

    def _executive_health_score(self):
        return self.executive_kpis._executive_health_score()

    def _ai_business_insights(self):
        return self.executive_kpis._ai_business_insights()

    def get_sales_kpis(self):
        return self.sales_kpis.get_sales_kpis()

    def get_product_kpis(self):
        return self.product_kpis.get_product_kpis()

    def get_channel_kpis(self):
        return self.channel_kpis.get_channel_kpis()

    def get_financial_kpis(self):
        return self.financial_kpis.get_financial_kpis()
