from datetime import date
from pydantic import BaseModel


class Reply(BaseModel):
    id: int
    content: str
    date: date
    topic_id: int
    user_id: int

class ReplyCreate(BaseModel):
    content: str
    topic_id: int
