from fastapi import APIRouter

from models.topic import TopicCreate, TopicResponse
from services.replies import RepliesService
from services.topics import TopicsService

router = APIRouter(tags=["topics"])


@router.post("/")
async def create_topic(topic: TopicCreate, token: str):
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
    TopicResponse
        The newly created topic.
    """
    return TopicsService.create_topic(topic, token)


# TODO:  Duplicated code-  get_topic

@router.get("/{topic_id}")
async def get_topic(token: str, topic_id: int):
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

    return TopicsService.get_topic(topic_id, token)


@router.get("/{topic_id}/replies")
async def get_topic(token: str, topic_id: int):
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


@router.get("/")
async def get_topics(token: str, search: str = None, sort: str = "DESC", page: int = 0, ):
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


@router.put("/{topic_id}/lock")
async def lock_topic(topic_id: int, token: str) -> bool:
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
    bool
        True if the topic was successfully locked.
    """

    return TopicsService.lock_topic_by_id(topic_id, token)
