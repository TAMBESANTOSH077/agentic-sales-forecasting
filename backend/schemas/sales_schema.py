from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ForecastRequest(BaseModel):

    region: Optional[str] = None

    category: Optional[str] = None

    forecast_days: int = Field(
        default=30,
        ge=7,
        le=90
    )


class AgentLog(BaseModel):

    agent: str

    status: str

    message: str


class ForecastResponse(BaseModel):

    status: str

    request: Dict[str, Any]

    forecast: Dict[str, Any]

    metrics: Dict[str, Any]

    insights: List[str]

    agent_logs: List[AgentLog]