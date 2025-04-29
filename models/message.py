from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int | None = None
    content: str
    date: datetime
    conversation_id: int
    sender_id: int
    receiver_id: int


class MessageCreate(BaseModel):
    content: str
    receiver_id: int
