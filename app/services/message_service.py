from sqlalchemy.orm import Session
from app.repositories import message_repository
from app.schemas.message import MessageCreate, MessageUpdate

def list_messages_by_conversation(db: Session, conversation_id: int, limit: int, offset: int):
    return message_repository.get_by_conversation_id(db, conversation_id, limit, offset)

def get_message(db: Session, message_id: int):
    return message_repository.get_by_id(db, message_id)

def create_message(db: Session, conversation_id: int, data: MessageCreate):
    return message_repository.create(db, conversation_id, data)

def update_message(db: Session, message_id: int, data: MessageUpdate):
    msg = message_repository.get_by_id(db, message_id)
    if not msg:
        return None
    return message_repository.update(db, msg, data)

def delete_message(db: Session, message_id: int):
    msg = message_repository.get_by_id(db, message_id)
    if not msg:
        return None
    message_repository.delete(db, msg)
    return True
