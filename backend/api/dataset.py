from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd
import io

from backend.database import get_db
from backend.models.customer import DatasetRun

router = APIRouter(prefix="/api/dataset", tags=["Dataset"])

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    return {"message": "Dataset uploaded successfully", "records": len(df)}

@router.get("/info")
def get_dataset_info(db: Session = Depends(get_db)):
    run = db.query(DatasetRun).order_by(DatasetRun.imported_at.desc()).first()
    if run:
        return run
    return {"message": "No dataset information available"}

@router.post("/import")
async def import_dataset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    run = DatasetRun(
        filename=file.filename,
        total_records=len(df),
        real_records=len(df),
        synthetic_records=0,
        valid_records=len(df),
        invalid_records=0
    )
    db.add(run)
    db.commit()
    return {"message": "Dataset imported successfully", "records": len(df)}

@router.get("/preview")
def preview_dataset():
    # Simplification: in real scenario, return from DB or raw file
    return {"items": []}

@router.get("/download-clean")
def download_clean():
    # Return a file
    return FileResponse("data/processed/clean_dataset.csv", filename="clean_dataset.csv")
