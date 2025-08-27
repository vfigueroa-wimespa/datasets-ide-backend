from pydantic import BaseModel
from typing import List, Literal

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class Conversation(BaseModel):
    messages: List[Message]
    title: str
