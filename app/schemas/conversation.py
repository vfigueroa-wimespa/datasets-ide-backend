from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ConversationBase(BaseModel):
    title: Optional[str] = None
    conversation_metadata: Optional[dict] = {}
    is_validated: Optional[bool] = False

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    conversation_metadata: Optional[dict]
    is_validated: Optional[bool]

class ConversationOut(ConversationBase):
    id: int
    dataset_id: int
    created_at: datetime

    class Config:
        orm_mode = True
