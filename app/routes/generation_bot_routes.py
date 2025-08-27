from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.generation_bot import (
    GenerationBotOut,
    GenerationBotCreate,
    GenerationBotUpdate,
)
from app.services import generation_bot_service
from typing import List

router = APIRouter(tags=["Generation Bots"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/datasets/{dataset_id}/bots", response_model=List[GenerationBotOut])
def list_bots(dataset_id: int, db: Session = Depends(get_db)):
    return generation_bot_service.list_bots(db, dataset_id)

@router.post("/datasets/{dataset_id}/bots", response_model=GenerationBotOut)
def create_bot(dataset_id: int, data: GenerationBotCreate, db: Session = Depends(get_db)):
    return generation_bot_service.create_bot(db, dataset_id, data)

@router.get("/bots/{bot_id}", response_model=GenerationBotOut)
def get_bot(bot_id: int, db: Session = Depends(get_db)):
    bot = generation_bot_service.get_bot(db, bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot

@router.put("/bots/{bot_id}", response_model=GenerationBotOut)
def update_bot(bot_id: int, data: GenerationBotUpdate, db: Session = Depends(get_db)):
    updated = generation_bot_service.update_bot(db, bot_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Bot not found")
    return updated

@router.delete("/bots/{bot_id}")
def delete_bot(bot_id: int, db: Session = Depends(get_db)):
    deleted = generation_bot_service.delete_bot(db, bot_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Bot not found")
    return {"ok": True}
