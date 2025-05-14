from fastapi import APIRouter

from models.reply import Reply, ReplyCreate
from services.replies import RepliesService

router = APIRouter(tags=["replies"])


@router.post("/best")
async def select_best_reply(reply_id: int, topic_id: int, token: str):
    """
    Mark a reply as the best answer for a specific topic.

    Parameters
    ----------
    reply_id : int
        The ID of the reply to be marked as best.
    topic_id : int
        The ID of the topic the reply belongs to.
    token : str
        Authentication token of the user making the request.

    Returns
    -------
    dict
        A response indicating whether the best reply was successfully set.
    """
    return RepliesService.set_best_reply(reply_id, topic_id, token)


@router.post("/vote")
async def vote_reply(reply_id: int, vote: int, token: str):
    """
    Cast a vote (upvote or downvote) on a reply.

    Parameters
    ----------
    reply_id : int
        The ID of the reply to vote on.
    vote : int
        The vote value (1 for upvote, 0 for downvote).
    token : str
        Authentication token of the voting user.

    Returns
    -------
    dict
        A response indicating the result of the vote operation.
    """
    return RepliesService.set_vote(reply_id, vote, token)

@router.post("/add/{topic_id}")
async def add_reply(token: str, topic_id: int, reply: ReplyCreate):
    """
    Add a new reply to a specific topic.

    Parameters
    ----------
    token : str
        Authentication token of the replying user.
    topic_id : int
        The ID of the topic to which the reply is being added.
    reply : ReplyCreate
        The reply content to be posted.

    Returns
    -------
    dict
        A response indicating whether the reply was successfully added.
    """
    return RepliesService.add_reply(reply.content, topic_id, token)