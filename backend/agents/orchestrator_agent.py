from dataclasses import dataclass, field
from typing import Any, Dict, List

from .data_collection_agent import collect_data
from .data_processing_agent import process_data
from .prediction_agent import predict_sales
from .verification_agent import verify_forecast
from .report_agent import generate_report


@dataclass
class AgentState:

    csv_path: str

    region: str | None = None

    category: str | None = None

    forecast_days: int = 30

    data: Any = None

    forecast: Dict[str, Any] = field(
        default_factory=dict
    )

    metrics: Dict[str, Any] = field(
        default_factory=dict
    )

    verification: Dict[str, Any] = field(
        default_factory=dict
    )

    insights: List[str] = field(
        default_factory=list
    )

    logs: List[Dict[str, str]] = field(
        default_factory=list
    )


def log_agent(
    state: AgentState,
    agent: str,
    status: str,
    message: str
):

    state.logs.append({

        "agent": agent,

        "status": status,

        "message": message
    })


def run_workflow(
    csv_path: str,
    region=None,
    category=None,
    forecast_days=30
):

    state = AgentState(
        csv_path=csv_path,
        region=region,
        category=category,
        forecast_days=forecast_days
    )

    # ==================================
    # 1. ORCHESTRATOR
    # ==================================

    log_agent(
        state,
        "Orchestrator",
        "running",
        "Received user goal and created execution plan."
    )

    # ==================================
    # 2. DATA COLLECTION
    # ==================================

    state.data = collect_data(
        csv_path
    )

    log_agent(
        state,
        "Data Collection Agent",
        "success",
        f"Loaded {len(state.data)} sales records."
    )

    # ==================================
    # 3. FILTER DATA
    # ==================================

    filtered_data = state.data.copy()

    if region:

        filtered_data = filtered_data[
            filtered_data["region"]
            .astype(str)
            .str.lower()
            == region.lower()
        ]

    if category:

        filtered_data = filtered_data[
            filtered_data["category"]
            .astype(str)
            .str.lower()
            == category.lower()
        ]

    if filtered_data.empty:

        raise ValueError(
            "No data found for the selected "
            "region/category."
        )

    # ==================================
    # 4. DATA PROCESSING
    # ==================================

    state.data = process_data(
        filtered_data
    )

    unique_days = (
        state.data["date"]
        .dt.date
        .nunique()
    )

    if unique_days < 14:

        raise ValueError(
            "Selected data contains fewer "
            "than 14 historical days."
        )

    log_agent(
        state,
        "Data Processing Agent",
        "success",
        (
            f"Cleaned and prepared "
            f"{len(state.data)} records "
            f"across {unique_days} days."
        )
    )

    # ==================================
    # 5. PREDICTION
    # ==================================

    state.forecast, state.metrics = (
        predict_sales(
            state.data,
            forecast_days
        )
    )

    log_agent(
        state,
        "Sales Prediction Agent",
        "success",
        (
            f"Generated {forecast_days}-day "
            "revenue forecast."
        )
    )

    # ==================================
    # 6. VERIFICATION
    # ==================================

    state.verification = (
        verify_forecast(
            state.data,
            state.forecast
        )
    )

    verification_status = (
        "success"
        if state.verification["passed"]
        else "warning"
    )

    log_agent(
        state,
        "Verification Agent",
        verification_status,
        state.verification["message"]
    )

    # ==================================
    # 7. REPORT
    # ==================================

    state.insights = generate_report(
        state.data,
        state.forecast,
        state.verification
    )

    log_agent(
        state,
        "Report Generation Agent",
        "success",
        "Generated executive business insights."
    )

    # ==================================
    # 8. COMPLETE
    # ==================================

    log_agent(
        state,
        "Orchestrator",
        "completed",
        "Multi-agent workflow completed."
    )

    return state