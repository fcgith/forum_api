from typing import List

from fastapi import APIRouter, Header

from models.reply import Reply
from models.topic import TopicCreate, Topic
from services.replies import RepliesService
from services.topics import TopicsService

router = APIRouter(tags=["topics"])


@router.post("/", response_model=dict)
async def create_topic(topic: TopicCreate,
                       token: str = Header(..., alias="Authorization")) -> dict:
    """
    Create a new topic.

    Parameters
    ----------
    topic : TopicCreate
        The topic details including title, content, and category ID.
    token : str
        Authentication token of the user creating the topic.

    Returns
    -------
    dict
        with topic ID and message indicating success.
    """
    return TopicsService.create_topic(topic, token)


# TODO:  Duplicated code-  get_topic

@router.get("/{topic_id}", response_model=Topic)
async def get_topic(topic_id: int,
                    token: str = Header(..., alias="Authorization")) -> Topic:
    """
    Retrieve a topic by its ID.

    Parameters
    ----------
    token : str
        Authentication token of the user.
    topic_id : int
        Unique identifier of the topic.

    Returns
    -------
    Topic
        The topic data.
    """

    return TopicsService.get_topic(topic_id, token)


@router.get("/{topic_id}/replies", response_model=List[Reply])
async def get_topic(topic_id: int,
                    token: str = Header(..., alias="Authorization")) -> List[Reply]:
    """
    Retrieve a topic by its ID.

    Parameters
    ----------
    token : str
        Authentication token of the user.
    topic_id : int
        Unique identifier of the topic.

    Returns
    -------
    TopicResponse
        The topic data.
    """
    return RepliesService.get_topic_replies(topic_id, token)


@router.get("/", response_model=dict)
async def get_topics(token: str = Header(..., alias="Authorization"),
                     search: str = None,
                     sort: str = "DESC",
                     page: int = 0) -> dict:
    """
    Retrieve a list of topics with optional filtering, sorting, and pagination.

    Parameters
    ----------
    token : str
        Authentication token of the user.
    search : str, optional
        Search keyword to filter topics by title or content.
    sort : str, default="DESC"
        Sort order for topics by creation date ('ASC' or 'DESC').
    page : int, default=0
        Page number for pagination.

    Returns
    -------
    TopicListResponse
        A list of topics with pagination metadata.
    """
    return TopicsService.get_topics(token=token, search=search, sort=sort, page=page)


@router.put("/{topic_id}/lock", response_model=dict)
async def lock_topic(topic_id: int,
                     token: str = Header(..., alias="Authorization")) -> dict:
    """
    Lock a topic to prevent further replies.

    Parameters
    ----------
    topic_id : int
        The ID of the topic to lock.
    token : str
        Authentication token of the requesting user.

    Returns
    -------
    dict
        Message indicating success or failure.
    """

    return TopicsService.lock_topic_by_id(topic_id, token)
