from fastapi import FastAPI

from Backend.config import MODEL_VER
# from db.database import init_db
# from routers import health, metrics, predict

# init_db()

app = FastAPI(title="Churn Prediction API", version=MODEL_VER)

# app.include_router(health.router)
# app.include_router(metrics.router)
# app.include_router(predict.router)