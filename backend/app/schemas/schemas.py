from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class CustomerBase(BaseModel):
    customer_id: str
    gender: str
    senior_citizen: int
    partner: str
    dependents: str
    tenure: int
    phone_service: str
    multiple_lines: str
    internet_service: str
    online_security: str
    online_backup: str
    device_protection: str
    tech_support: str
    streaming_tv: str
    streaming_movies: str
    contract: str
    paperless_billing: str
    payment_method: str
    monthly_charges: float
    total_charges: float
    
class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    data_source: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    risk_level: str
    prediction: str
    model_version: str

class AnalyticsOverview(BaseModel):
    total_customers: int
    predicted_churn: int
    high_risk: int
    critical_risk: int
    average_probability: float
    model_accuracy: float
    
class CustomerSearchResponse(BaseModel):
    data: List[Dict[str, Any]]
    total: int
    page: int
    limit: int
