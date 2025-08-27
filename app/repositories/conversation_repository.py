from sqlalchemy.orm import Session
from app.db import models
from app.schemas.conversation import ConversationCreate, ConversationUpdate

def get_by_dataset_id(db: Session, dataset_id: int, limit: int, offset: int):
    return (
        db.query(models.Conversation)
        .filter(models.Conversation.dataset_id == dataset_id)
        .order_by(models.Conversation.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

def get_by_id(db: Session, conversation_id: int):
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def create(db: Session, dataset_id: int, data: ConversationCreate):
    convo = models.Conversation(dataset_id=dataset_id, **data.dict())
    db.add(convo)
    db.commit()
    db.refresh(convo)
    return convo

def update(db: Session, convo: models.Conversation, data: ConversationUpdate):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(convo, field, value)
    db.commit()
    db.refresh(convo)
    return convo

def delete(db: Session, convo: models.Conversation):
    db.delete(convo)
    db.commit()
