from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from backend.models.customer import Customer, Prediction
import pandas as pd

class CustomerService:
    def get_customers(self, db: Session, search: str = None, risk_level: str = None, 
                      contract: str = None, internet_service: str = None, 
                      payment_method: str = None, min_tenure: int = None, max_tenure: int = None,
                      min_charges: float = None, max_charges: float = None,
                      sort_by: str = None, sort_order: str = 'asc', page: int = 1, limit: int = 10) -> dict:
        query = db.query(Customer)
        
        if search:
            query = query.filter(Customer.customer_id.ilike(f"%{search}%"))
        if contract:
            query = query.filter(Customer.contract == contract)
        if internet_service:
            query = query.filter(Customer.internet_service == internet_service)
        if payment_method:
            query = query.filter(Customer.payment_method == payment_method)
        if min_tenure is not None:
            query = query.filter(Customer.tenure >= min_tenure)
        if max_tenure is not None:
            query = query.filter(Customer.tenure <= max_tenure)
        if min_charges is not None:
            query = query.filter(Customer.monthly_charges >= min_charges)
        if max_charges is not None:
            query = query.filter(Customer.monthly_charges <= max_charges)

        if risk_level:
            query = query.join(Prediction, Customer.customer_id == Prediction.customer_id)\
                         .filter(Prediction.risk_level == risk_level)

        total = query.count()

        if sort_by:
            if hasattr(Customer, sort_by):
                column = getattr(Customer, sort_by)
                query = query.order_by(desc(column) if sort_order == 'desc' else asc(column))

        items = query.offset((page - 1) * limit).limit(limit).all()
        return {"items": items, "total": total, "page": page, "limit": limit}

    def get_customer_by_id(self, db: Session, customer_id: str) -> dict:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if not customer:
            return None
        prediction = db.query(Prediction).filter(Prediction.customer_id == customer_id).order_by(desc(Prediction.predicted_at)).first()
        customer_dict = {c.name: getattr(customer, c.name) for c in customer.__table__.columns}
        if prediction:
            customer_dict['prediction'] = {p.name: getattr(prediction, p.name) for p in prediction.__table__.columns}
        return customer_dict

    def get_high_risk_customers(self, db: Session, limit: int = 10) -> list:
        return db.query(Customer).join(Prediction, Customer.customer_id == Prediction.customer_id)\
                 .filter(Prediction.risk_level.in_(['High', 'Critical']))\
                 .order_by(desc(Prediction.churn_probability))\
                 .limit(limit).all()

    def import_customers(self, db: Session, df: pd.DataFrame) -> dict:
        records = df.to_dict(orient='records')
        count = 0
        for record in records:
            if not db.query(Customer).filter(Customer.customer_id == record['customer_id']).first():
                db.add(Customer(**record))
                count += 1
        db.commit()
        return {"imported": count, "total": len(records)}

    def get_customer_count(self, db: Session) -> int:
        return db.query(Customer).count()

customer_service = CustomerService()
