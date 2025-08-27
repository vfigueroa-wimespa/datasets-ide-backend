from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class GenerationBotConfig(Base):
    __tablename__ = "generation_bot_configs"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    
    name = Column(String, nullable=False)  # nombre visible en frontend
    system_prompt = Column(Text, nullable=False)
    user_role = Column(String, default="user")
    generation_style = Column(String, default="instructivo")
    model_name = Column(String, default="gpt-4o-mini")
    temperature = Column(Float, default=0.7)
    max_turns = Column(Integer, default=6)

    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", backref="generation_bots")
