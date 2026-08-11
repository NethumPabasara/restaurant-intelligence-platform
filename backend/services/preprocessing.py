import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


class DataLoader:

    def __init__(self):

        # Load environment variables from backend/.env
        load_dotenv()

        # Get Supabase database URL
        DATABASE_URL = os.getenv("DATABASE_URL")

        if not DATABASE_URL:
            raise ValueError("DATABASE_URL not found in .env")

        # Create database connection
        self.engine = create_engine(DATABASE_URL)

        # DataFrames
        self.sales = None
        self.digital_channels = None
        self.aggregator = None
        self.deliveroo = None
        self.epos_summary = None
        self.epos_mix = None
        self.pnl = None

    def load_all_data(self):

        print("=" * 60)
        print("Loading Restaurant Intelligence Data from Supabase...")
        print("=" * 60)

        # Restaurant Sales
        self.sales = pd.read_sql_table(
            "Anonymized_Restaurant_Sales_Data",
            self.engine
        )

        # Digital Channels
        self.digital_channels = pd.read_sql_table(
            "Public_DigitalChannels_Monthly_Revenue_FinancialYear",
            self.engine
        )

        # Aggregator
        self.aggregator = pd.read_sql_table(
            "Public_Aggregator_Monthly_Revenue_FinancialYear",
            self.engine
        )

        # Deliveroo
        self.deliveroo = pd.read_sql_table(
            "Public_Deliveroo_Category_Summary_2023_2025",
            self.engine
        )

        # EPOS Summary
        self.epos_summary = pd.read_sql_table(
            "Public_EPOS_Category_Summary_2023_2025",
            self.engine
        )

        # EPOS Mix
        self.epos_mix = pd.read_sql_table(
            "Public_EPOS_Annual_Category_Mix_2023_2025",
            self.engine
        )

        # Profit & Loss
        self.pnl = pd.read_sql_table(
            "Public_Derived_Consolidated_PnL_2023_2025",
            self.engine
        )

        print("All datasets loaded successfully from Supabase.\n")

        print("Dataset Summary")
        print("-" * 60)

        datasets = {
            "Sales": self.sales,
            "Digital Channels": self.digital_channels,
            "Aggregator": self.aggregator,
            "Deliveroo": self.deliveroo,
            "EPOS Summary": self.epos_summary,
            "EPOS Mix": self.epos_mix,
            "PnL": self.pnl
        }

        for name, df in datasets.items():

            print(
                f"{name:<20} "
                f"Rows: {len(df):>6} | "
                f"Columns: {len(df.columns)}"
            )

        print("=" * 60)

        return datasets


if __name__ == "__main__":

    loader = DataLoader()
    loader.load_all_data()