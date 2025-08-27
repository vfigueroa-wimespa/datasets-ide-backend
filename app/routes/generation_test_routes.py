from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.generation_service import generate_and_store_one
from app.schemas.conversation import ConversationOut

router = APIRouter(tags=["Generation Test"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/bots/{bot_id}/generate-test", response_model=ConversationOut)
def generate_test(bot_id: int, db: Session = Depends(get_db)):
    try:
        convo = generate_and_store_one(bot_id, db)
        return convo
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
