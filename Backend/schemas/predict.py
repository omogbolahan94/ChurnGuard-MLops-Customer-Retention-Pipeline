from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

from Backend.config import (
    VALID_PLAN_TYPES,
    P99_SESSION, P99_LOGINS, P99_FEATURES, P99_PAGES, P99_TICKETS,
)


class PredictRequest(BaseModel):
    customer_id: str
    session_duration_sec: float = Field(..., ge=0)
    pages_viewed: int = Field(..., ge=0)
    support_tickets: int = Field(..., ge=0)
    days_inactive: int = Field(..., ge=0, le=365)
    login_count_30d: int = Field(..., ge=0)
    features_used: int = Field(..., ge=0)
    plan_type: str
    threshold_override: Optional[float] = None

    @field_validator("session_duration_sec")
    @classmethod
    def cap_session(cls, v: float) -> float:
        return min(v, 3600)

    @field_validator("plan_type")
    @classmethod
    def valid_plan(cls, v: str) -> str:
        if v not in VALID_PLAN_TYPES:
            raise ValueError(
                f"plan_type must be one of: {sorted(VALID_PLAN_TYPES)}. Got: '{v}'"
            )
        return v

    def to_feature_dict(self) -> dict:
        engagement = (
            (self.session_duration_sec / P99_SESSION) * 0.3
            + (min(self.login_count_30d, P99_LOGINS) / P99_LOGINS) * 0.3
            + (min(self.features_used, P99_FEATURES) / P99_FEATURES) * 0.2
            + (min(self.pages_viewed, P99_PAGES) / P99_PAGES) * 0.2
        )

        risk = (
            (self.days_inactive / 90) * 0.4
            + (min(self.support_tickets, P99_TICKETS) / P99_TICKETS) * 0.3
            + (1 - engagement) * 0.3
        )

        tickets_per_login = (
            self.support_tickets /
            (self.login_count_30d + 1)
        )

        if self.days_inactive <= 7:
            recency = "active"
        elif self.days_inactive <= 14:
            recency = "at_risk"
        elif self.days_inactive <= 30:
            recency = "dormant"
        else:
            recency = "churning"

        return {
            "session_duration_sec": self.session_duration_sec,
            "pages_viewed": self.pages_viewed,
            "support_tickets": self.support_tickets,
            "days_inactive": self.days_inactive,
            "login_count_30d": self.login_count_30d,
            "features_used": self.features_used,
            "engagement_score": round(min(engagement, 1.0), 4),
            "risk_score": round(min(risk, 1.0), 4),
            "tickets_per_login": round(tickets_per_login, 4),
            "plan_type": self.plan_type,
            "recency_bucket": recency,
        }


class BatchPredictRequest(BaseModel):
    customers: List[PredictRequest]