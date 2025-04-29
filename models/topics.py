from datetime import datetime
from pydantic import BaseModel


class Topic(BaseModel):
    id: int
    name: str
    content: str
    date: datetime
    category_id: int
    user_id: int


class TopicCreate(BaseModel):
    name: str
    content: str
    category_id: int


class TopicResponse(Topic):
    pass
