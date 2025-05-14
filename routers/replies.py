from fastapi import APIRouter

from models.reply import Reply, ReplyCreate
from services.replies import RepliesService

router = APIRouter(tags=["replies"])


@router.post("/best")
async def select_best_reply(reply_id: int, topic_id: int, token: str):
    """
    Choose the best reply for a topic

    - Requires authentication
    - Only the topic author can select the best reply to their topic
    """
    return RepliesService.set_best_reply(reply_id, topic_id, token)


@router.post("/vote")
async def vote_reply(reply_id: int, vote: int, token: str):
    """
    Upvote or downvote a reply

    - Requires authentication
    - vote=1 for upvote, vote=0 for downvote
    - A user can change their vote but can only vote once per reply
    """
    return RepliesService.set_vote(reply_id, vote, token)

@router.post("/add/{topic_id}")
async def add_reply(token: str, topic_id: int, reply: ReplyCreate):
    return RepliesService.add_reply(reply.content, topic_id, token)