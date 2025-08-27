from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DatasetBase(BaseModel):
    name: str
    description: Optional[str] = None
    version: Optional[str] = "v1"
    tags: Optional[List[str]] = []

class DatasetCreate(DatasetBase):
    pass

class DatasetUpdate(BaseModel):
    description: Optional[str]
    version: Optional[str]
    tags: Optional[List[str]]

class DatasetOut(DatasetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
