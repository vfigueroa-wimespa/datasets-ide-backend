from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class EnqueueCountIn(BaseModel):
    count: int = Field(gt=0, le=10000)
    priority: int = 100

class EnqueueCountOut(BaseModel):
    batch_id: int
    enqueued: int

class BatchProgress(BaseModel):
    batch_id: int
    total: int
    queued: int
    running: int
    done: int
    failed: int

class QueueJobOut(BaseModel):
    id: int
    batch_id: int
    status: str
    priority: int
    attempts: int
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
