from sqlalchemy.orm import Session
from app.repositories import generation_bot_repository
from app.schemas.generation_bot import GenerationBotCreate, GenerationBotUpdate

def list_bots(db: Session, dataset_id: int):
    return generation_bot_repository.list_by_dataset(db, dataset_id)

def get_bot(db: Session, bot_id: int):
    return generation_bot_repository.get_by_id(db, bot_id)

def create_bot(db: Session, dataset_id: int, data: GenerationBotCreate):
    return generation_bot_repository.create(db, dataset_id, data)

def update_bot(db: Session, bot_id: int, data: GenerationBotUpdate):
    bot = generation_bot_repository.get_by_id(db, bot_id)
    if not bot:
        return None
    return generation_bot_repository.update(db, bot, data)

def delete_bot(db: Session, bot_id: int):
    bot = generation_bot_repository.get_by_id(db, bot_id)
    if not bot:
        return None
    generation_bot_repository.delete(db, bot)
    return True
