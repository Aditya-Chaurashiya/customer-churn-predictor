from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import pandas as pd
import io

from backend.app.database import get_db
from backend.app.models.models import Customer, Prediction, ModelVersion
from backend.app.schemas.schemas import CustomerCreate, PredictionResponse, AnalyticsOverview, CustomerSearchResponse
from backend.app.services.prediction_service import prediction_service

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    model_loaded = prediction_service.model is not None
    db_connected = False
    try:
        db.execute("SELECT 1")
        db_connected = True
    except:
        pass
        
    return {
        "status": "healthy",
        "database": "connected" if db_connected else "disconnected",
        "model": "loaded" if model_loaded else "unloaded",
        "model_version": prediction_service.metadata.get("model_version", "unknown") if model_loaded else "unknown"
    }

@router.post("/predict", response_model=PredictionResponse)
def predict_single(customer: CustomerCreate, db: Session = Depends(get_db)):
    customer_dict = customer.dict()
    # Map pydantic fields to match pandas expected names
    data = {
        "customerID": customer_dict["customer_id"],
        "gender": customer_dict["gender"],
        "SeniorCitizen": customer_dict["senior_citizen"],
        "Partner": customer_dict["partner"],
        "Dependents": customer_dict["dependents"],
        "tenure": customer_dict["tenure"],
        "PhoneService": customer_dict["phone_service"],
        "MultipleLines": customer_dict["multiple_lines"],
        "InternetService": customer_dict["internet_service"],
        "OnlineSecurity": customer_dict["online_security"],
        "OnlineBackup": customer_dict["online_backup"],
        "DeviceProtection": customer_dict["device_protection"],
        "TechSupport": customer_dict["tech_support"],
        "StreamingTV": customer_dict["streaming_tv"],
        "StreamingMovies": customer_dict["streaming_movies"],
        "Contract": customer_dict["contract"],
        "PaperlessBilling": customer_dict["paperless_billing"],
        "PaymentMethod": customer_dict["payment_method"],
        "MonthlyCharges": customer_dict["monthly_charges"],
        "TotalCharges": customer_dict["total_charges"],
    }
    
    result = prediction_service.predict_single(data)
    
    # Store prediction
    pred = Prediction(
        customer_id=result["customer_id"],
        churn_probability=result["churn_probability"],
        risk_level=result["risk_level"],
        prediction=result["prediction"],
        model_version=result["model_version"]
    )
    db.add(pred)
    db.commit()
    
    return result

@router.post("/predict/batch")
async def predict_batch(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
        
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    results = prediction_service.predict_batch(df)
    
    # Optional: save batch results to DB
    
    # For now, just return results
    return {"results": results}

@router.get("/customers", response_model=CustomerSearchResponse)
def get_customers(
    risk: Optional[str] = None,
    contract: Optional[str] = None,
    internet_service: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Customer, Prediction).outerjoin(
        Prediction, Customer.customer_id == Prediction.customer_id
    )
    
    if risk:
        query = query.filter(Prediction.risk_level == risk)
    if contract:
        query = query.filter(Customer.contract == contract)
    if internet_service:
        query = query.filter(Customer.internet_service == internet_service)
        
    total = query.count()
    
    # Ordering by risk descending (just using churn_probability)
    query = query.order_by(Prediction.churn_probability.desc().nullslast())
    
    offset = (page - 1) * limit
    results = query.offset(offset).limit(limit).all()
    
    data = []
    for cust, pred in results:
        item = {
            "customer_id": cust.customer_id,
            "contract": cust.contract,
            "tenure": cust.tenure,
            "internet_service": cust.internet_service,
            "monthly_charges": cust.monthly_charges,
            "churn_probability": pred.churn_probability if pred else None,
            "risk": pred.risk_level if pred else "Unknown",
            "prediction": pred.prediction if pred else "Unknown"
        }
        data.append(item)
        
    return {
        "data": data,
        "total": total,
        "page": page,
        "limit": limit
    }

@router.get("/analytics/overview", response_model=AnalyticsOverview)
def get_analytics_overview(db: Session = Depends(get_db)):
    total_customers = db.query(Customer).count()
    predicted_churn = db.query(Prediction).filter(Prediction.prediction == "Likely to Churn").count()
    high_risk = db.query(Prediction).filter(Prediction.risk_level == "High Risk").count()
    critical_risk = db.query(Prediction).filter(Prediction.risk_level == "Critical Risk").count()
    
    avg_prob = db.query(func.avg(Prediction.churn_probability)).scalar() or 0.0
    
    latest_model = db.query(ModelVersion).order_by(ModelVersion.created_at.desc()).first()
    accuracy = latest_model.accuracy if latest_model else 0.0
    
    return {
        "total_customers": total_customers,
        "predicted_churn": predicted_churn,
        "high_risk": high_risk,
        "critical_risk": critical_risk,
        "average_probability": round(avg_prob, 4),
        "model_accuracy": accuracy
    }

@router.get("/analytics/charts")
def get_analytics_charts(db: Session = Depends(get_db)):
    # Simple aggregations
    
    # Risk Distribution
    risk_dist = db.query(Prediction.risk_level, func.count(Prediction.id)).group_by(Prediction.risk_level).all()
    
    # Contract Dist
    contract_dist = db.query(Customer.contract, func.count(Customer.id)).group_by(Customer.contract).all()
    
    # Internet Service
    internet_dist = db.query(Customer.internet_service, func.count(Customer.id)).group_by(Customer.internet_service).all()
    
    return {
        "risk_distribution": [{"name": k, "value": v} for k, v in risk_dist if k],
        "contract_distribution": [{"name": k, "value": v} for k, v in contract_dist],
        "internet_distribution": [{"name": k, "value": v} for k, v in internet_dist]
    }
