from datetime import date
from pydantic import BaseModel


class Reply(BaseModel):
    id: int
    content: str
    date: date
    topic_id: int
    user_id: int
    best_reply: int = 0
    user_name: str = "Error fetching username"
    likes: int = 0

class ReplyCreate(BaseModel):
    content: str
