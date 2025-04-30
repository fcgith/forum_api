from typing import List
from fastapi import APIRouter
from models.message import MessageCreate
from models.user import UserPublic
from services.conversations import ConversationsService

router = APIRouter(tags=["conversations"])


@router.get("/")
async def get_all_conversations(token: str)-> List[UserPublic]:
    """
    Get all users with whom the authenticated user has exchanged messages

    - Requires authentication via token
    """
    return ConversationsService.get_conversations(token)


@router.post("/messages")
async def send_message(message: MessageCreate, token: str):
    """
    Create a new message in an existing conversation or start a new conversation if none exists yet.

    - Requires authentication via token
    - Message must contain text content
    """
    return ConversationsService.send_message(message.receiver_id, message.content, token)



@router.get("/{conversation_id}")
async def get_conversation_messages(conversation_id: int, token: str):
    """
    Get all messages in a conversation

    - Requires authentication via token
    - User must be part of the conversation
    """
    return ConversationsService.get_conversation_messages(conversation_id, token)