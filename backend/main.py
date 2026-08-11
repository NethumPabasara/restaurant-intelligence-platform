from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services.preprocessing import DataLoader
from backend.services.kpi_engine import KPIEngine

app = FastAPI(
    title="Restaurant Intelligence Platform",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Load datasets
# -------------------------------

loader = DataLoader()
loader.load_all_data()

# -------------------------------
# Initialize KPI Engine
# -------------------------------

kpi_engine = KPIEngine(loader)


@app.get("/")
def home():

    return {
        "message": "Restaurant Intelligence Platform API"
    }


@app.get("/api/executive")
def executive_dashboard():

    return kpi_engine.get_executive_kpis()

@app.get("/api/sales")
def sales_dashboard():

    return kpi_engine.get_sales_kpis()

@app.get("/api/product")
def product_dashboard():

    return kpi_engine.get_product_kpis()

@app.get("/api/channel")
def channel_dashboard():

    return kpi_engine.get_channel_kpis()

@app.get("/api/financial")
def financial_dashboard():

    return kpi_engine.get_financial_kpis()