from sqlalchemy.orm import Session
from app.repositories import conversation_repository
from app.schemas.conversation import ConversationCreate, ConversationUpdate

def list_conversations_by_dataset(db: Session, dataset_id: int, limit: int, offset: int):
    return conversation_repository.get_by_dataset_id(db, dataset_id, limit, offset)

def get_conversation(db: Session, conversation_id: int):
    return conversation_repository.get_by_id(db, conversation_id)

def create_conversation(db: Session, dataset_id: int, data: ConversationCreate):
    return conversation_repository.create(db, dataset_id, data)

def update_conversation(db: Session, conversation_id: int, data: ConversationUpdate):
    convo = conversation_repository.get_by_id(db, conversation_id)
    if not convo:
        return None
    return conversation_repository.update(db, convo, data)

def delete_conversation(db: Session, conversation_id: int):
    convo = conversation_repository.get_by_id(db, conversation_id)
    if not convo:
        return None
    conversation_repository.delete(db, convo)
    return True
