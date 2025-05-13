from fastapi import APIRouter

from models.topic import TopicCreate, TopicResponse
from services.replies import RepliesService
from services.topics import TopicsService

router = APIRouter(tags=["topics"])


@router.post("/")
async def create_topic(topic: TopicCreate, token: str):
    """
    Create a new topic

    - Requires authentication token
    - Topic data must contain at least a title and a Category
    """
    return TopicsService.create_topic(topic, token)


@router.get("/{topic_id}")
async def get_topic(token: str,topic_id: int):
    """
    Get a topic by ID
    """
    return TopicsService.get_topic(topic_id,token)

@router.get("/{topic_id}/replies")
async def get_topic(token: str,topic_id: int):
    """
    Get a topic by ID
    """
    return RepliesService.get_topic_replies(topic_id, token)

@router.get("/")
async def get_topics(token: str,search:str=None,sort:str="DESC",page:int=0,):
    """
    Get all topics
    """
    return TopicsService.get_topics(token=token, search=search, sort=sort, page=page)

@router.put("/{topic_id}/lock")
async def lock_topic(topic_id: int, token: str) -> bool:
    return TopicsService.lock_topic_by_id(topic_id, token)