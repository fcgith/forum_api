import unittest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from models.message import MessageCreate
from models.user import UserPublic
from routers import conversations as conversations_router
from services.errors import invalid_token, conversation_not_found, invalid_credentials

# Create a mock for the ConversationsService
mock_conversations_service = Mock(spec='services.conversations.ConversationsService')

# Replace the actual service with the mock in the router
conversations_router.ConversationsService = mock_conversations_service


def fake_user():
    user = Mock()
    user.id = 1
    user.username = "testuser"
    user.avatar = "avatar.jpg"
    user.creation_date = "2023-01-01"
    return user


def fake_message():
    message = Mock()
    message.id = 1
    message.content = "Test message"
    message.conversation_id = 1
    message.sender_id = 1
    message.receiver_id = 2
    message.date = "2023-01-01"
    return message


class ConversationsRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        mock_conversations_service.reset_mock()

    async def test_getAllConversations_returnsListOfUsers_whenTokenIsValid(self):
        # Arrange
        test_token = "valid_token"
        expected_users = [fake_user()]

        mock_conversations_service.get_conversations.return_value = expected_users

        # Act
        result = await conversations_router.get_all_conversations(test_token)

        # Assert
        self.assertEqual(expected_users, result)
        mock_conversations_service.get_conversations.assert_called_once_with(test_token)

    async def test_getAllConversations_raisesException_whenServiceRaisesInvalidToken(self):
        # Arrange
        test_token = "invalid_token"

        mock_conversations_service.get_conversations.side_effect = invalid_token

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await conversations_router.get_all_conversations(test_token)

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual("Invalid token", context.exception.detail)
        mock_conversations_service.get_conversations.assert_called_once_with(test_token)

    async def test_sendMessage_returnsSuccessResponse_whenMessageIsValid(self):
        # Arrange
        test_token = "valid_token"
        test_message = MessageCreate(content="Test message", receiver_id=2)
        expected_response = {"message_id": 1, "message": "Message sent successfully"}

        mock_conversations_service.send_message.return_value = expected_response

        # Act
        result = await conversations_router.send_message(test_message, test_token)

        # Assert
        self.assertEqual(expected_response, result)
        mock_conversations_service.send_message.assert_called_once_with(
            test_message.receiver_id, test_message.content, test_token
        )

    async def test_sendMessage_raisesException_whenServiceRaisesInvalidToken(self):
        # Arrange
        test_token = "invalid_token"
        test_message = MessageCreate(content="Test message", receiver_id=2)

        mock_conversations_service.send_message.side_effect = invalid_token

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await conversations_router.send_message(test_message, test_token)

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual("Invalid token", context.exception.detail)
        mock_conversations_service.send_message.assert_called_once_with(
            test_message.receiver_id, test_message.content, test_token
        )

    async def test_sendMessage_raisesException_whenServiceRaisesInvalidCredentials(self):
        # Arrange
        test_token = "valid_token"
        test_message = MessageCreate(content="Test message", receiver_id=1)  # Sending to self

        mock_conversations_service.send_message.side_effect = invalid_credentials

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await conversations_router.send_message(test_message, test_token)

        self.assertEqual(403, context.exception.status_code)
        self.assertEqual("Invalid credentials", context.exception.detail)
        mock_conversations_service.send_message.assert_called_once_with(
            test_message.receiver_id, test_message.content, test_token
        )

    async def test_getConversationMessages_returnsListOfMessages_whenConversationExists(self):
        # Arrange
        test_token = "valid_token"
        test_conversation_id = 1
        expected_messages = [fake_message()]

        mock_conversations_service.get_conversation_messages.return_value = expected_messages

        # Act
        result = await conversations_router.get_conversation_messages(test_conversation_id, test_token)

        # Assert
        self.assertEqual(expected_messages, result)
        mock_conversations_service.get_conversation_messages.assert_called_once_with(test_conversation_id, test_token)

    async def test_getConversationMessages_raisesException_whenServiceRaisesInvalidToken(self):
        # Arrange
        test_token = "invalid_token"
        test_conversation_id = 1

        mock_conversations_service.get_conversation_messages.side_effect = invalid_token

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await conversations_router.get_conversation_messages(test_conversation_id, test_token)

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual("Invalid token", context.exception.detail)
        mock_conversations_service.get_conversation_messages.assert_called_once_with(test_conversation_id, test_token)

    async def test_getConversationMessages_raisesException_whenServiceRaisesConversationNotFound(self):
        # Arrange
        test_token = "valid_token"
        test_conversation_id = 999

        mock_conversations_service.get_conversation_messages.side_effect = conversation_not_found

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await conversations_router.get_conversation_messages(test_conversation_id, test_token)

        self.assertEqual(402, context.exception.status_code)
        self.assertEqual("Conversation not found", context.exception.detail)
        mock_conversations_service.get_conversation_messages.assert_called_once_with(test_conversation_id, test_token)

    async def test_getConversationMessages_raisesException_whenServiceRaisesInvalidCredentials(self):
        # Arrange
        test_token = "valid_token"
        test_conversation_id = 1

        mock_conversations_service.get_conversation_messages.side_effect = invalid_credentials

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await conversations_router.get_conversation_messages(test_conversation_id, test_token)

        self.assertEqual(403, context.exception.status_code)
        self.assertEqual("Invalid credentials", context.exception.detail)
        mock_conversations_service.get_conversation_messages.assert_called_once_with(test_conversation_id, test_token)


if __name__ == '__main__':
    unittest.main()