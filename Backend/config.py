from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent

MODEL_PATH = f"{ROOT_DIR}/models/churn_model_v1.joblib"
DB_PATH = f"{ROOT_DIR}/models/prediction_log.db"
MODEL_VER  = "v1.0"

NUMERIC_FEATURES = [
    "session_duration_sec", "pages_viewed", "support_tickets",
    "days_inactive", "login_count_30d", "features_used",
    "engagement_score", "risk_score", "tickets_per_login",
]

CATEGORICAL_FEATURES = ["plan_type", "recency_bucket"]

VALID_PLAN_TYPES = {"free", "basic", "pro"}

# Percentile caps captured at training time
P99_SESSION  = 540.0
P99_LOGINS   = 40.0
P99_FEATURES = 12.0
P99_PAGES    = 15.0
P99_TICKETS  = 3.0 