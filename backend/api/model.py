from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.prediction_service import prediction_service
from backend.models.customer import ModelVersion

router = APIRouter(prefix="/api/model", tags=["Model"])

@router.get("/info")
def get_model_info():
    return prediction_service.get_model_info()

@router.post("/retrain")
def retrain_model(data_path: str = "data/raw/dataset.csv"):
    metrics = prediction_service.retrain_model(data_path)
    return {"message": "Model retrained successfully", "metrics": metrics}

@router.get("/versions")
def get_model_versions(db: Session = Depends(get_db)):
    versions = db.query(ModelVersion).order_by(ModelVersion.created_at.desc()).all()
    return versions
