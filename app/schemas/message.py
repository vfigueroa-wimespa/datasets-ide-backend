from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

# 👇 Enum compatible con Pydantic y FastAPI
class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"

class MessageBase(BaseModel):
    role: RoleEnum
    content: str
    position: int

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: str

class MessageOut(MessageBase):
    id: int
    conversation_id: int
    created_at: datetime

    class Config:
        orm_mode = True
