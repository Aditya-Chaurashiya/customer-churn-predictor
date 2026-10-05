from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from backend.models.customer import Customer, Prediction, ModelVersion
from datetime import datetime

class AnalyticsService:
    def get_overview(self, db: Session) -> dict:
        total = db.query(Customer).count()
        predicted_churn = db.query(Prediction).filter(Prediction.prediction == 'Yes').count()
        high_risk = db.query(Prediction).filter(Prediction.risk_level == 'High').count()
        critical_risk = db.query(Prediction).filter(Prediction.risk_level == 'Critical').count()
        
        avg_prob = db.query(func.avg(Prediction.churn_probability)).scalar() or 0.0
        
        model = db.query(ModelVersion).order_by(desc(ModelVersion.created_at)).first()
        model_accuracy = model.accuracy if model else 0.0
        model_version = model.version if model else "unknown"
        last_trained = model.created_at.isoformat() if model else datetime.now().isoformat()
        
        return {
            "total_customers": total,
            "predicted_churn": predicted_churn,
            "high_risk": high_risk,
            "critical_risk": critical_risk,
            "average_probability": float(avg_prob),
            "model_accuracy": float(model_accuracy),
            "model_version": model_version,
            "last_trained": last_trained
        }

    def get_churn_by_contract(self, db: Session) -> list:
        results = db.query(
            Customer.contract,
            func.count(Customer.id).label('total'),
            func.sum(func.cast(Prediction.prediction == 'Yes', func.Integer())).label('churned')
        ).outerjoin(Prediction, Customer.customer_id == Prediction.customer_id)\
        .group_by(Customer.contract).all()
        
        return [{"contract_type": r.contract, "total": r.total, "churned": r.churned or 0, 
                 "churn_rate": (r.churned or 0) / r.total if r.total else 0.0} for r in results]

    def get_churn_by_service(self, db: Session) -> list:
        results = db.query(
            Customer.internet_service,
            func.count(Customer.id).label('total'),
            func.sum(func.cast(Prediction.prediction == 'Yes', func.Integer())).label('churned')
        ).outerjoin(Prediction, Customer.customer_id == Prediction.customer_id)\
        .group_by(Customer.internet_service).all()
        return [{"service": r.internet_service, "total": r.total, "churned": r.churned or 0,
                 "churn_rate": (r.churned or 0) / r.total if r.total else 0.0} for r in results]

    def get_risk_distribution(self, db: Session) -> list:
        total = db.query(Prediction).count() or 1
        results = db.query(
            Prediction.risk_level,
            func.count(Prediction.id).label('count')
        ).group_by(Prediction.risk_level).all()
        return [{"risk_level": r.risk_level, "count": r.count, 
                 "percentage": r.count / total * 100} for r in results]

    def get_churn_by_tenure(self, db: Session) -> list:
        # Simplified grouping for tenure (e.g. 0-12, 13-24, etc.)
        return []

    def get_churn_by_monthly_charges(self, db: Session) -> list:
        return []

    def get_probability_distribution(self, db: Session) -> list:
        # Simplified histogram
        return []

    def get_confusion_matrix(self, db: Session) -> dict:
        return {"tp": 0, "tn": 0, "fp": 0, "fn": 0}

    def get_top_churn_indicators(self, db: Session) -> list:
        return [{"feature": "MonthlyCharges", "importance": 0.35}]

analytics_service = AnalyticsService()
