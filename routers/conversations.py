from typing import List
from fastapi import APIRouter
from models.message import MessageCreate
from models.user import UserPublic
from services.conversations import ConversationsService

router = APIRouter(tags=["conversations"])


@router.get("/")
async def get_all_conversations(token: str)-> List[UserPublic]:
    """
    Retrieve all users the authenticated user has had conversations with.

    Parameters
    ----------
    token : str
        Authentication token identifying the requesting user.

    Returns
    -------
    List[UserPublic]
        A list of users with whom the authenticated user has exchanged messages.
    """
    return ConversationsService.get_conversations(token)


@router.post("/messages")
async def send_message(message: MessageCreate, token: str):
    """
    Send a message to another user. Starts a new conversation if one does not exist.

    Parameters
    ----------
    message : MessageCreate
        Contains the receiver's ID and message content.
    token : str
        Authentication token of the sending user.

    Returns
    -------
    dict
        A response indicating the success or failure of the message delivery.
    """
    return ConversationsService.send_message(message.receiver_id, message.content, token)



@router.get("/{conversation_id}")
async def get_conversation_messages(conversation_id: int, token: str):
    """
    Retrieve all messages in a specific conversation.

    Parameters
    ----------
    conversation_id : int
        The ID of the conversation to retrieve.
    token : str
        Authentication token of the requesting user.

    Returns
    -------
    List[dict]
        A list of messages in the specified conversation.
    """
    return ConversationsService.get_conversation_messages(conversation_id, token)