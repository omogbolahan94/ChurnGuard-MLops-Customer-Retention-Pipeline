import sqlite3
import json
from datetime import datetime, timezone

from Backend.config import DB_PATH, MODEL_VER 
from Backend.models.loader import THRESHOLD


# ── Prediction log (SQLite locally, BigQuery in prod) ──────
def init_db() -> None:
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id     TEXT,
            churn_prob      REAL,
            predicted_label INTEGER,
            threshold_used  REAL,
            model_version   TEXT,
            scored_at       TEXT,
            features_json   TEXT
        )
    """)
    con.commit()
    con.close()


def log_prediction(customer_id: str, prob: float, label: int, features_dict: dict) -> None:
    con = sqlite3.connect(DB_PATH)
    con.execute(
        """
        INSERT INTO predictions
            (customer_id, churn_prob, predicted_label,
             threshold_used, model_version, scored_at, features_json)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (customer_id, prob, label, THRESHOLD, MODEL_VER,
         datetime.now(timezone.utc).isoformat(), json.dumps(features_dict)),
    )
    con.commit()
    con.close()