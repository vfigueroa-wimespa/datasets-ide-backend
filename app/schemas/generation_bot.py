from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GenerationBotBase(BaseModel):
    name: str
    system_prompt: str
    user_role: Optional[str] = "user"
    generation_style: Optional[str] = "instructivo"
    model_name: Optional[str] = "gpt-4o-mini"
    temperature: Optional[float] = 0.7
    max_turns: Optional[int] = 6

class GenerationBotCreate(GenerationBotBase):
    pass

class GenerationBotUpdate(BaseModel):
    name: Optional[str]
    system_prompt: Optional[str]
    user_role: Optional[str]
    generation_style: Optional[str]
    model_name: Optional[str]
    temperature: Optional[float]
    max_turns: Optional[int]

class GenerationBotOut(GenerationBotBase):
    id: int
    dataset_id: int
    created_at: datetime

    class Config:
        orm_mode = True
