from typing import List

from fastapi import APIRouter
from models.message import MessageRequest, NewConversationRequest
from models.user import UserPublic
from services.conversations import ConversationsService

router = APIRouter(tags=["conversations"])


@router.get("/")
async def get_all_conversations(token: str):
    """
    Get all users with whom the authenticated user has exchanged messages

    - Requires authentication via token
    """
    return ConversationsService.get_conversations(token)


@router.post("/{conversation_id}/messages")
async def send_message(conversation_id: int, message: MessageRequest, token: str):
    """
    Create a new message in an existing conversation

    - Requires authentication via token
    - Message must contain text content
    - User must be part of the conversation
    """
    return ConversationsService.send_message(conversation_id, message.content, token)


@router.post("/")
async def create_conversation(conversation: NewConversationRequest, token: str):
    """
    Create a new conversation with a user and send the first message

    - Requires authentication via token
    - Message must contain text content
    - Receiver must be a valid user
    """
    return ConversationsService.create_conversation_and_send_message(
        conversation.receiver_id,
        conversation.content,
        token
    )


@router.get("/{conversation_id}/messages")
async def get_conversation_messages(conversation_id: int, token: str):
    """
    Get all messages in a conversation

    - Requires authentication via token
    - User must be part of the conversation
    """
    return ConversationsService.get_conversation_messages(conversation_id, token)