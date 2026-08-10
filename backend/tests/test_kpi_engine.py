import unittest

import pandas as pd

from backend.services.kpi_engine import KPIEngine
from backend.services.executive_kpis import ExecutiveKPIs
from backend.services.sales_kpis import SalesKPIs
from backend.services.product_kpis import ProductKPIs
from backend.services.channel_kpis import ChannelKPIs
from backend.services.financial_kpis import FinancialKPIs


class DummyLoader:
    def __init__(self):
        self.sales = pd.DataFrame(
            [{
                "Date": "01/01/2024",
                "OrderID": 1,
                "Gross Sales": 100.0,
                "Est. Profit": 40.0,
                "Quantity": 2,
                "Category": "Burger",
                "Payment": "Card",
                "OrderType": "Delivery",
                "Time": "18:00"
            }]
        )
        self.digital_channels = pd.DataFrame({"Month": ["2024-01"], "Revenue": [50.0]})
        self.aggregator = pd.DataFrame({"Month": ["2024-01"], "Revenue": [25.0]})
        self.deliveroo = pd.DataFrame()
        self.epos_summary = pd.DataFrame()
        self.epos_mix = pd.DataFrame()
        self.pnl = pd.DataFrame({"Month": ["2024-01"], "Labour": [10.0], "Rent": [5.0]})


class KPIEngineCompositionTest(unittest.TestCase):
    def test_engine_initializes_modular_kpi_components(self):
        engine = KPIEngine(DummyLoader())

        self.assertIsInstance(engine.executive_kpis, ExecutiveKPIs)
        self.assertIsInstance(engine.sales_kpis, SalesKPIs)
        self.assertIsInstance(engine.product_kpis, ProductKPIs)
        self.assertIsInstance(engine.channel_kpis, ChannelKPIs)
        self.assertIsInstance(engine.financial_kpis, FinancialKPIs)


if __name__ == "__main__":
    unittest.main()
