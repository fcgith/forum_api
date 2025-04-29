from repo.conversation import get_conversation_by_id, create_conversation, \
    conversation_exists, get_conversations_by_user, get_conversation_by_users
from repo.message import create_message, get_messages_by_conversation
import repo.user  as user_repo
from models.message import MessageCreate
from models.conversation import ConversationCreate
from services.errors import invalid_token, not_found, invalid_token, conversation_not_found, invalid_credentials
from services.utils import AuthToken


class ConversationsService:
    @classmethod
    def get_conversations(cls, token: str):
        """
        Get all users with whom the authenticated user has exchanged messages

        Args:
            token: Authentication token

        Returns:
            List of users
        """
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token
        conversations = get_conversations_by_user(user.id)
        users = []
        for conversation in conversations:
            if conversation.initiator_id == user.id and conversation.receiver_id not in users:
                users.append(conversation.receiver_id)
            elif conversation.receiver_id ==user.id and conversation.initiator_id not in users:
                users.append(conversation.initiator_id)
        return user_repo.get_users_in_list_by_id(users,True)

    @classmethod
    def send_message(cls, receiver_id: int, content: str, token: str):
        """
        Send a message to an existing conversation

        Args:
            content: Text content of the message
            token: Authentication token

        Returns:
            Dictionary with message ID and status
        """
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token
        receiver_user = user_repo.get_user_by_id(receiver_id)
        if not receiver_user:
            raise invalid_credentials
        if receiver_id==user.id:
            raise invalid_credentials
        if not conversation_exists(user.id, receiver_id):
            conversation_id = create_conversation(user.id, receiver_id)
        else:
            conversation_id=get_conversation_by_users(user.id,receiver_id)


        message_data = MessageCreate(
            content=content,
            receiver_id=receiver_id
        )

        message_id = create_message(message_data,conversation_id,user.id)
        return {"message_id": message_id, "status": "Message sent successfully"}


    @classmethod
    def get_conversation_messages(cls, conversation_id: int, token: str):
        """
        Get all messages in a conversation

        Args:
            conversation_id: ID of the conversation
            token: Authentication token

        Returns:
            List of messages
        """
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token

        conversation = get_conversation_by_id(conversation_id)
        if not conversation:
            raise conversation_not_found

        if user.id not in ( conversation.initiator_id , conversation.receiver_id):
            raise invalid_credentials

        messages = get_messages_by_conversation(conversation_id)
        return messages