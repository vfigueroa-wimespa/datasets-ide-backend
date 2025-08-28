from sqlalchemy.orm import Session
from app.db import models
from app.schemas.dataset import DatasetCreate, DatasetUpdate

def get_all(db: Session):
    return db.query(models.Dataset).all()

def get_by_id(db: Session, dataset_id: int):
    return db.query(models.Dataset).filter(models.Dataset.id == dataset_id).first()

def create(db: Session, data: DatasetCreate):
    dataset = models.Dataset(**data.dict())
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return dataset

def update(db: Session, dataset: models.Dataset, data: DatasetUpdate):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(dataset, field, value)
    db.commit()
    db.refresh(dataset)
    return dataset

def delete(db: Session, dataset: models.Dataset):
    db.delete(dataset)
    db.commit()


def get_dataset_with_conversations(db: Session, dataset_id: int):
    dataset = (
        db.query(models.Dataset)
        .filter(models.Dataset.id == dataset_id)
        .first()
    )
    if not dataset:
        return None

    conversations = []
    for conv in dataset.conversations:
        messages = sorted(conv.messages, key=lambda m: m.position)
        conversations.append([
            {"role": m.role.value, "content": m.content}
            for m in messages
        ])

    return {
        "id": dataset.id,
        "name": dataset.name,
        "description": dataset.description,
        "version": dataset.version,
        "conversations": conversations,
    }