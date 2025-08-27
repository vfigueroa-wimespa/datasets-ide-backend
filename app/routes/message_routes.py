from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.message import (
    MessageCreate,
    MessageUpdate,
    MessageOut,
)
from app.services import message_service

router = APIRouter(tags=["Messages"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageOut])
def list_messages(
    conversation_id: int,
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    return message_service.list_messages_by_conversation(db, conversation_id, limit, offset)

@router.post("/conversations/{conversation_id}/messages", response_model=MessageOut)
def create_message(conversation_id: int, data: MessageCreate, db: Session = Depends(get_db)):
    return message_service.create_message(db, conversation_id, data)

@router.get("/messages/{message_id}", response_model=MessageOut)
def get_message(message_id: int, db: Session = Depends(get_db)):
    msg = message_service.get_message(db, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg

@router.put("/messages/{message_id}", response_model=MessageOut)
def update_message(message_id: int, data: MessageUpdate, db: Session = Depends(get_db)):
    updated = message_service.update_message(db, message_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Message not found")
    return updated

@router.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    deleted = message_service.delete_message(db, message_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"ok": True}
