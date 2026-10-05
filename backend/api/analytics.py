from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend.schemas.customer import AnalyticsOverview, ChurnByContract, RiskDistribution, ModelMetrics
from backend.services.analytics_service import analytics_service

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])

@router.get("/overview", response_model=AnalyticsOverview)
def get_overview(db: Session = Depends(get_db)):
    return analytics_service.get_overview(db)

@router.get("/churn-by-contract", response_model=List[ChurnByContract])
def get_churn_by_contract(db: Session = Depends(get_db)):
    return analytics_service.get_churn_by_contract(db)

@router.get("/churn-by-service")
def get_churn_by_service(db: Session = Depends(get_db)):
    return analytics_service.get_churn_by_service(db)

@router.get("/risk-distribution", response_model=List[RiskDistribution])
def get_risk_distribution(db: Session = Depends(get_db)):
    return analytics_service.get_risk_distribution(db)

@router.get("/churn-by-tenure")
def get_churn_by_tenure(db: Session = Depends(get_db)):
    return analytics_service.get_churn_by_tenure(db)

@router.get("/churn-by-monthly-charges")
def get_churn_by_monthly_charges(db: Session = Depends(get_db)):
    return analytics_service.get_churn_by_monthly_charges(db)

@router.get("/probability-distribution")
def get_probability_distribution(db: Session = Depends(get_db)):
    return analytics_service.get_probability_distribution(db)

@router.get("/confusion-matrix")
def get_confusion_matrix(db: Session = Depends(get_db)):
    return analytics_service.get_confusion_matrix(db)

@router.get("/top-indicators")
def get_top_indicators(db: Session = Depends(get_db)):
    return analytics_service.get_top_churn_indicators(db)

@router.get("/model-performance")
def get_model_performance(db: Session = Depends(get_db)):
    # simplified mock
    return {
        "version": "1.0.0",
        "accuracy": 0.85,
        "precision_score": 0.82,
        "recall": 0.78,
        "f1_score": 0.80,
        "roc_auc": 0.88,
        "training_records": 5000,
        "created_at": "2023-10-01T00:00:00"
    }
