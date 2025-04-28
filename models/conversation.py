from datetime import datetime
from pydantic import BaseModel


class Conversation(BaseModel):
    id: int | None = None
    date: datetime
    initiator_id: int
    receiver_id: int


class ConversationCreate(BaseModel):
    initiator_id: int
    receiver_id: int