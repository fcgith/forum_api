from datetime import datetime
from pydantic import BaseModel


class Conversation(BaseModel):
    id: int | None = None
    date: datetime
    initiator_id: int
    receiver_id: int
    seen: int = 0


class ConversationCreate(BaseModel):
    initiator_id: int
    receiver_id: int
