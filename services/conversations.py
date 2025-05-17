from typing import List

import repo.conversation as conversation_repo
import repo.message as message_repo
import repo.user as user_repo
from models.message import MessageCreate, Message
from services.errors import invalid_token, not_found, invalid_token, conversation_not_found, invalid_credentials
from services.utils import AuthToken


class ConversationsService:
    @classmethod
    def get_last_message(cls, user_id: int, token: str) -> Message:
        user = AuthToken.validate(token)
        user2 = user_repo.get_user_by_id(user_id)
        if not user2:
            raise not_found

        last_message = user_repo.get_last_message_between(user, user2)

        if not last_message.get("id"):
            raise not_found

        return last_message

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
        conversations = conversation_repo.get_conversations_by_user(user.id)

        users = []
        for conversation in conversations:
            if conversation.initiator_id == user.id and conversation.receiver_id not in users:
                users.append(conversation.receiver_id)
            elif conversation.receiver_id == user.id and conversation.initiator_id not in users:
                users.append(conversation.initiator_id)

        return user_repo.get_users_in_list_by_id(users, True)

    @classmethod
    def send_message(cls, receiver_id: int, content: str, token: str):
        """
        Send a message to an existing conversation or start a new conversation if none exists yet.

        Args:
            content: Text content of the message
            receiver_id: ID of the user to whom the message is being sent
            token: Authentication token

        Returns:
            Dictionary with message ID and status
        """
        user = AuthToken.validate(token)
        receiver_user = user_repo.get_user_by_id(receiver_id)

        if not receiver_user or receiver_id == user.id:
            raise invalid_credentials

        if not conversation_repo.conversation_exists(user.id, receiver_id):
            conversation_id = conversation_repo.create_conversation(user.id, receiver_id)
        else:
            conversation_id = conversation_repo.get_conversation_by_users(user.id, receiver_id)

        message_data = MessageCreate(
            content=content,
            receiver_id=receiver_id
        )

        message_id = message_repo.create_message(message_data, conversation_id, user.id)
        return {"message_id": message_id, "message": "Message sent successfully"}

    @classmethod
    def get_conversation_messages(cls, conversation_id: int, token: str) -> List[Message]:
        """
        Get all messages in a conversation

        Args:
            conversation_id: ID of the conversation
            token: Authentication token

        Returns:
            List of messages
        """
        user = AuthToken.validate(token)

        conversation = conversation_repo.get_conversation_by_id(conversation_id)
        if not conversation:
            raise conversation_not_found

        if user.id not in (conversation.initiator_id, conversation.receiver_id):
            raise invalid_credentials

        messages = message_repo.get_messages_by_conversation(conversation_id)

        if not messages:
            raise not_found

        return messages

    @classmethod
    def get_messages_between(cls, user_id, token) -> List[Message]:
        user1 = AuthToken.validate(token)
        user2 = user_repo.get_user_by_id(user_id)
        if not user2:
            raise not_found

        conversation = conversation_repo.get_conversation_between_users(user1.id, user2.id)
        if not conversation:
            raise not_found

        messages = message_repo.get_messages_by_conversation(conversation.id)
        return messages
