from sqlalchemy.orm import Session
from app.db.generation_models import GenerationBotConfig
from app.schemas.generation_bot import GenerationBotCreate, GenerationBotUpdate

def list_by_dataset(db: Session, dataset_id: int):
    return db.query(GenerationBotConfig).filter_by(dataset_id=dataset_id).all()

def get_by_id(db: Session, bot_id: int):
    return db.query(GenerationBotConfig).filter_by(id=bot_id).first()

def create(db: Session, dataset_id: int, data: GenerationBotCreate):
    bot = GenerationBotConfig(dataset_id=dataset_id, **data.dict())
    db.add(bot)
    db.commit()
    db.refresh(bot)
    return bot

def update(db: Session, bot: GenerationBotConfig, data: GenerationBotUpdate):
    for field, value in data.dict(exclude_unset=True).items():
        setattr(bot, field, value)
    db.commit()
    db.refresh(bot)
    return bot

def delete(db: Session, bot: GenerationBotConfig):
    db.delete(bot)
    db.commit()
