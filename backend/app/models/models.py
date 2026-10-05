from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from backend.app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), unique=True, index=True)
    gender = Column(String(20))
    senior_citizen = Column(Integer)
    partner = Column(String(10))
    dependents = Column(String(10))
    tenure = Column(Integer)
    phone_service = Column(String(10))
    multiple_lines = Column(String(50))
    internet_service = Column(String(50))
    online_security = Column(String(50))
    online_backup = Column(String(50))
    device_protection = Column(String(50))
    tech_support = Column(String(50))
    streaming_tv = Column(String(50))
    streaming_movies = Column(String(50))
    contract = Column(String(50))
    paperless_billing = Column(String(10))
    payment_method = Column(String(50))
    monthly_charges = Column(Float)
    total_charges = Column(Float)
    data_source = Column(String(20), default="real")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String(50), index=True)
    churn_probability = Column(Float)
    risk_level = Column(String(20))
    prediction = Column(String(20))
    model_version = Column(String(20))
    predicted_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    version = Column(String(20), unique=True, index=True)
    accuracy = Column(Float)
    precision = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    roc_auc = Column(Float)
    training_records = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
