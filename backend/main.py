from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from backend.config import settings
from backend.database import init_db
from backend.api import health, predictions, customers, analytics, model, dataset
from backend.services.prediction_service import prediction_service

app = FastAPI(
    title="CustomerChurnPredictor API",
    description="Predictive Customer Analytics Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Response-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def startup_event():
    init_db()
    # Force model load
    _ = prediction_service

app.include_router(health.router)
app.include_router(predictions.router)
app.include_router(customers.router)
app.include_router(analytics.router)
app.include_router(model.router)
app.include_router(dataset.router)
