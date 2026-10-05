from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime, timezone
from backend.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(50), unique=True, index=True)
    gender = Column(String(20))
    senior_citizen = Column(Integer)
    partner = Column(String(10))
    dependents = Column(String(10))
    tenure = Column(Integer)
    phone_service = Column(String(10))
    multiple_lines = Column(String(30))
    internet_service = Column(String(30))
    online_security = Column(String(30))
    online_backup = Column(String(30))
    device_protection = Column(String(30))
    tech_support = Column(String(30))
    streaming_tv = Column(String(30))
    streaming_movies = Column(String(30))
    contract = Column(String(30))
    paperless_billing = Column(String(10))
    payment_method = Column(String(50))
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    churn = Column(String(10), nullable=True)
    data_source = Column(String(20), default='real')
    created_at = Column(DateTime, default=utcnow)

class Prediction(Base):
    __tablename__ = 'predictions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(50), index=True)
    churn_probability = Column(Float)
    risk_level = Column(String(20))
    prediction = Column(String(30))
    model_version = Column(String(20))
    predicted_at = Column(DateTime, default=utcnow)

class ModelVersion(Base):
    __tablename__ = 'model_versions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(20))
    accuracy = Column(Float)
    precision_score = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    roc_auc = Column(Float)
    training_records = Column(Integer)
    validation_records = Column(Integer)
    test_records = Column(Integer)
    created_at = Column(DateTime, default=utcnow)

class DatasetRun(Base):
    __tablename__ = 'dataset_runs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255))
    total_records = Column(Integer)
    real_records = Column(Integer)
    synthetic_records = Column(Integer)
    valid_records = Column(Integer)
    invalid_records = Column(Integer)
    imported_at = Column(DateTime, default=utcnow)
