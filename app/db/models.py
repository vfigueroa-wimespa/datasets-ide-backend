# app/db/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
import enum

class RoleEnum(enum.Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(Text)
    version = Column(String, default="v1")
    tags = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    conversations = relationship("Conversation", back_populates="dataset")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    title = Column(String, nullable=True)
    conversation_metadata = Column(JSON, default={})  # <--- CAMBIO AQUÍ
    is_validated = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    dataset = relationship("Dataset", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    role = Column(Enum(RoleEnum))
    content = Column(Text)
    position = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")
