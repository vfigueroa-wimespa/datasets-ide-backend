from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.conversation import (
    ConversationOut,
    ConversationCreate,
    ConversationUpdate,
)
from app.services import conversation_service
from typing import List

router = APIRouter(tags=["Conversations"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/datasets/{dataset_id}/conversations", response_model=List[ConversationOut])
def list_conversations(
    dataset_id: int,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return conversation_service.list_conversations_by_dataset(db, dataset_id, limit, offset)

@router.post("/datasets/{dataset_id}/conversations", response_model=ConversationOut)
def create_conversation(
    dataset_id: int,
    data: ConversationCreate,
    db: Session = Depends(get_db)
):
    return conversation_service.create_conversation(db, dataset_id, data)

@router.get("/conversations/{conversation_id}", response_model=ConversationOut)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    convo = conversation_service.get_conversation(db, conversation_id)
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return convo

@router.put("/conversations/{conversation_id}", response_model=ConversationOut)
def update_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    db: Session = Depends(get_db)
):
    updated = conversation_service.update_conversation(db, conversation_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return updated

@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    deleted = conversation_service.delete_conversation(db, conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"ok": True}
