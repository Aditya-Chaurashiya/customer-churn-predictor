from fastapi import APIRouter, Depends, Query, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import pandas as pd
import io

from backend.database import get_db
from backend.services.customer_service import customer_service

router = APIRouter(prefix="/api/customers", tags=["Customers"])

@router.get("")
def list_customers(
    search: Optional[str] = None,
    risk: Optional[str] = None,
    contract: Optional[str] = None,
    internet_service: Optional[str] = None,
    payment_method: Optional[str] = None,
    min_tenure: Optional[int] = None,
    max_tenure: Optional[int] = None,
    min_charges: Optional[float] = None,
    max_charges: Optional[float] = None,
    sort_by: Optional[str] = None,
    sort_order: str = 'asc',
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return customer_service.get_customers(
        db, search, risk, contract, internet_service, payment_method,
        min_tenure, max_tenure, min_charges, max_charges, sort_by, sort_order, page, limit
    )

@router.get("/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = customer_service.get_customer_by_id(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/import")
async def import_customers(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    result = customer_service.import_customers(db, df)
    return result
