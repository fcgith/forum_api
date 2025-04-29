from datetime import date
from pydantic import BaseModel


class Topic(BaseModel):
    id: int
    name: str
    content: str
    date: date
    category_id: int
    user_id: int


class TopicCreate(BaseModel):
    name: str
    content: str
    category_id: int


class TopicResponse(Topic):
    content: str
