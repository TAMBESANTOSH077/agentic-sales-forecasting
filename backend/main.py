from pathlib import Path
import shutil

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from agents.orchestrator_agent import run_workflow


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"

DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

DEFAULT_DATA = DATA_DIR / "sales_data.csv"


app = FastAPI(
    title="Agentic AI Sales Forecasting API",
    description="Multi-Agent AI system for sales forecasting",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Agentic Sales Forecasting API",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/forecast")
async def forecast(
    region: str | None = Form(default=None),
    category: str | None = Form(default=None),
    forecast_days: int = Form(default=30),
    file: UploadFile | None = File(default=None),
):

    try:

        if forecast_days < 7 or forecast_days > 90:
            raise HTTPException(
                status_code=400,
                detail="forecast_days must be between 7 and 90."
            )

        # -------------------------
        # DATA SOURCE
        # -------------------------

        if file:

            if not file.filename:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid file."
                )

            if not file.filename.lower().endswith(".csv"):
                raise HTTPException(
                    status_code=400,
                    detail="Only CSV files are supported."
                )

            safe_name = Path(file.filename).name
            path = UPLOAD_DIR / safe_name

            with path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        else:

            path = DEFAULT_DATA

        # -------------------------
        # RUN MULTI-AGENT SYSTEM
        # -------------------------

        state = run_workflow(
            csv_path=str(path),
            region=region,
            category=category,
            forecast_days=forecast_days
        )

        # -------------------------
        # RESPONSE
        # -------------------------

        return {
            "status": "success",

            "request": {
                "region": region,
                "category": category,
                "forecast_days": forecast_days
            },

            "forecast": {
                **state.forecast,
                "verification": state.verification
            },

            "metrics": state.metrics,

            "insights": state.insights,

            "agent_logs": state.logs
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )