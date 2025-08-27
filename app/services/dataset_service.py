from sqlalchemy.orm import Session
from app.repositories import dataset_repository
from app.schemas.dataset import DatasetCreate, DatasetUpdate

def list_datasets(db: Session):
    return dataset_repository.get_all(db)

def get_dataset(db: Session, dataset_id: int):
    return dataset_repository.get_by_id(db, dataset_id)

def create_dataset(db: Session, data: DatasetCreate):
    return dataset_repository.create(db, data)

def update_dataset(db: Session, dataset_id: int, data: DatasetUpdate):
    dataset = dataset_repository.get_by_id(db, dataset_id)
    if not dataset:
        return None
    return dataset_repository.update(db, dataset, data)

def delete_dataset(db: Session, dataset_id: int):
    dataset = dataset_repository.get_by_id(db, dataset_id)
    if not dataset:
        return None
    dataset_repository.delete(db, dataset)
    return True
