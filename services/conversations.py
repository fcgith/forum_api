from repo.conversation import get_conversation_by_id, get_conversations_by_user, create_conversation
from repo.message import create_message, get_messages_by_conversation
from repo.user import get_user_by_id
from models.message import MessageCreate
from models.conversation import ConversationCreate
from services.errors import access_denied, not_found
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
            raise access_denied
        conversations = get_conversations_by_user(user.id)
        users = []
        for conversation in conversations:
            if conversation.initiator_id == user.id:
                users.append(get_user_by_id(conversation.receiver_id))
            else:
                users.append(get_user_by_id(conversation.initiator_id))
        return users

    @classmethod
    def send_message(cls, conversation_id: int, content: str, token: str):
        """
        Send a message to an existing conversation

        Args:
            conversation_id: ID of the conversation
            content: Text content of the message
            token: Authentication token

        Returns:
            Dictionary with message ID and status
        """
        user = AuthToken.validate(token)
        if not user:
            raise access_denied

        conversation = get_conversation_by_id(conversation_id)
        if not conversation:
            raise not_found

        if user.id != conversation.initiator_id and user.id != conversation.receiver_id:
            raise access_denied

        message_data = MessageCreate(
            content=content,
            conversation_id=conversation_id,
            sender_id=user.id
        )

        message_id = create_message(message_data)
        return {"message_id": message_id, "status": "Message sent successfully"}

    @classmethod
    def create_conversation_and_send_message(cls, receiver_id: int, content: str, token: str):
        """
        Create a new conversation with a user and send the first message

        Args:
            receiver_id: ID of the user to start conversation with
            content: Text content of the message
            token: Authentication token

        Returns:
            Dictionary with conversation ID, message ID and status
        """
        user = AuthToken.validate(token)
        if not user:
            raise access_denied

        receiver = get_user_by_id(receiver_id)
        if not receiver:
            raise not_found

        conversation_data = ConversationCreate(
            initiator_id=user.id,
            receiver_id=receiver_id
        )

        conversation_id = create_conversation(conversation_data)

        message_data = MessageCreate(
            content=content,
            conversation_id=conversation_id,
            sender_id=user.id
        )

        message_id = create_message(message_data)
        return {"conversation_id": conversation_id, "message_id": message_id, "status": "Message sent successfully"}

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
            raise access_denied

        conversation = get_conversation_by_id(conversation_id)
        if not conversation:
            raise not_found

        if user.id != conversation.initiator_id and user.id != conversation.receiver_id:
            raise access_denied

        messages = get_messages_by_conversation(conversation_id)
        return messages