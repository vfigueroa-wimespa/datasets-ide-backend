from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.dataset import DatasetOut, DatasetCreate, DatasetUpdate
from app.services import dataset_service

router = APIRouter(prefix="/datasets", tags=["Datasets"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[DatasetOut])
def list_datasets(db: Session = Depends(get_db)):
    return dataset_service.list_datasets(db)

@router.post("/", response_model=DatasetOut)
def create_dataset(data: DatasetCreate, db: Session = Depends(get_db)):
    return dataset_service.create_dataset(db, data)

@router.get("/{dataset_id}", response_model=DatasetOut)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    dataset = dataset_service.get_dataset(db, dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.put("/{dataset_id}", response_model=DatasetOut)
def update_dataset(dataset_id: int, data: DatasetUpdate, db: Session = Depends(get_db)):
    updated = dataset_service.update_dataset(db, dataset_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return updated

@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    deleted = dataset_service.delete_dataset(db, dataset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return {"ok": True}
