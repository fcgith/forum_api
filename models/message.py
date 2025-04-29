from datetime import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int | None = None
    content: str
    date: datetime
    conversation_id: int
    sender_id: int


class MessageCreate(BaseModel):
    content: str
    conversation_id: int
    sender_id: int

class MessageRequest(BaseModel):
    content: str


class NewConversationRequest(BaseModel):
    receiver_id: int
    content: str