from fastapi import APIRouter

from services.conversations import ConversationsService

router = APIRouter(tags=["conversations"])
@router.get("/")
async def get_all_conversations(token:str):
    return ConversationsService.get_conversations(token)
