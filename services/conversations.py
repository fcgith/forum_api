from repo.conversation import get_conversation_by_id, get_conversations_by_user
from repo.user import get_user_by_username, get_user_by_id
from services.errors import access_denied
from services.utils import AuthToken


class ConversationsService:
    @classmethod
    def get_conversations(cls, token: str):
        user=AuthToken.validate(token)
        if not user:
            raise access_denied
        conversations = get_conversations_by_user(user.id)
        users=[]
        for conversation in conversations:
            if conversation.initiator_id == user.id:
                users.append(get_user_by_id(conversation.receiver_id))
            else:
                users.append(get_user_by_id(conversation.initiator_id))
        return users
