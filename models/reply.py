from datetime import datetime
from pydantic import BaseModel



class Reply(BaseModel):
    id: int
    content: str
    date: datetime
    topic_id: int
    user_id: int

class ReplyCreate(BaseModel):
    content: str
    topic_id: int
