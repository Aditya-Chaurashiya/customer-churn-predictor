from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io

from backend.database import get_db
from backend.schemas.customer import PredictionRequest, PredictionResponse, BatchPredictionResponse
from backend.services.prediction_service import prediction_service
from backend.models.customer import Prediction, Customer

router = APIRouter(prefix="/api", tags=["Predictions"])

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, db: Session = Depends(get_db)):
    result = prediction_service.predict_single(request.dict())
    
    # Store in DB
    pred_record = Prediction(
        customer_id=result['customer_id'],
        churn_probability=result['churn_probability'],
        risk_level=result['risk_level'],
        prediction=result['prediction'],
        model_version=result['model_version']
    )
    db.add(pred_record)
    db.commit()
    
    return result

@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    results = prediction_service.predict_batch(df)
    
    # Store in DB
    for res in results:
        pred_record = Prediction(
            customer_id=res.get('customer_id', 'unknown'),
            churn_probability=res['churn_probability'],
            risk_level=res['risk_level'],
            prediction=res['prediction'],
            model_version=res['model_version']
        )
        db.add(pred_record)
    db.commit()
    
    return BatchPredictionResponse(
        total=len(results),
        processed=len(results),
        results=results
    )

@router.get("/predictions", response_model=dict)
def get_predictions(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    preds = db.query(Prediction).offset((page - 1) * limit).limit(limit).all()
    total = db.query(Prediction).count()
    return {"items": [p.__dict__ for p in preds], "total": total, "page": page, "limit": limit}

@router.get("/predictions/{customer_id}")
def get_prediction_by_customer(customer_id: str, db: Session = Depends(get_db)):
    pred = db.query(Prediction).filter(Prediction.customer_id == customer_id).order_by(Prediction.predicted_at.desc()).first()
    if not pred:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return pred
