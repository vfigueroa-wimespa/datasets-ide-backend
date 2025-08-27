from sqlalchemy.orm import Session
from app.db import models
from app.schemas.message import MessageCreate, MessageUpdate

def get_by_conversation_id(db: Session, conversation_id: int, limit: int, offset: int):
    return (
        db.query(models.Message)
        .filter(models.Message.conversation_id == conversation_id)
        .order_by(models.Message.position.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

def get_by_id(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()

def create(db: Session, conversation_id: int, data: MessageCreate):
    msg = models.Message(conversation_id=conversation_id, **data.dict())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

def update(db: Session, message: models.Message, data: MessageUpdate):
    message.content = data.content
    db.commit()
    db.refresh(message)
    return message

def delete(db: Session, message: models.Message):
    db.delete(message)
    db.commit()
