from typing import List
from fastapi import APIRouter, Header
from models.message import MessageCreate, Message
from models.user import UserPublic
from services.conversations import ConversationsService

router = APIRouter(tags=["conversations"])


@router.get("/")
async def get_all_conversations(token: str = Header(..., alias="Authorization")) -> List[UserPublic]:
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


@router.get("/last-message/{user_id}", response_model=Message)
async def get_last_message(user_id: int,
                           token: str = Header(..., alias="Authorization")) -> Message:
    """
    Gets the last message in the conversation between a user and authenticated user.

    Parameters
    ----------
    user_id : User ID
        Contains the ID of the unauthenticated user.
    token : str
        Authentication token

    Returns
    -------
    dict
        Last message details.
    """
    return ConversationsService.get_last_message(user_id, token)


@router.post("/messages/")
async def send_message(message: MessageCreate, token: str = Header(..., alias="Authorization")):
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


@router.get("/{conversation_id}", response_model=List[Message])
async def get_conversation_messages(conversation_id: int,
                                    token: str = Header(..., alias="Authorization")) -> List[Message]:
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


@router.get("/msg/{user_id}", response_model=List[Message])
async def get_messages_beetween(user_id: int,
                                token: str = Header(..., alias="Authorization")) -> List[Message]:
    """
    Gets the messages between two users with user ID and authentication token.

    Parameters
    ----------
    user_id : second user ID
        Contains the receiver's ID and message content.
    token : str
        Authentication token of first user.

    Returns
    -------
    dict
        Returns a dict of messages between the two users.
    """
    return ConversationsService.get_messages_between(user_id, token)
