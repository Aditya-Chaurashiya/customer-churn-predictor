from pydantic import BaseModel, ConfigDict
from typing import List, Optional
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
    churn: Optional[str] = None
    data_source: Optional[str] = 'real'

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CustomerListResponse(BaseModel):
    items: List[CustomerResponse]
    total: int
    page: int
    limit: int

class PredictionRequest(BaseModel):
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

class PredictionResponse(BaseModel):
    customer_id: str
    churn_probability: float
    risk_level: str
    prediction: str
    model_version: str
    risk_factors: List[str]
    protective_factors: List[str]

class BatchPredictionResponse(BaseModel):
    total: int
    processed: int
    results: List[PredictionResponse]

class AnalyticsOverview(BaseModel):
    total_customers: int
    predicted_churn: int
    high_risk: int
    critical_risk: int
    average_probability: float
    model_accuracy: float
    model_version: str
    last_trained: str

class ChurnByContract(BaseModel):
    contract_type: str
    total: int
    churned: int
    churn_rate: float

class RiskDistribution(BaseModel):
    risk_level: str
    count: int
    percentage: float

class ModelMetrics(BaseModel):
    version: str
    accuracy: float
    precision_score: float
    recall: float
    f1_score: float
    roc_auc: float
    training_records: int
    created_at: datetime

class DatasetInfo(BaseModel):
    source: str
    total_records: int
    real_records: int
    synthetic_records: int
    columns: int
    missing_values: int
    duplicate_ids: int
    target_distribution: dict

class HealthResponse(BaseModel):
    status: str
    database: bool
    model: bool
    model_version: str
