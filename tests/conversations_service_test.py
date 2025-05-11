import unittest
from unittest.mock import Mock, patch

from models.message import MessageCreate
from services.conversations import ConversationsService
from services.errors import invalid_token, conversation_not_found, invalid_credentials


class TestConversationsService(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.valid_token = "valid_token"
        self.invalid_token = "invalid_token"

        # Create mock user
        self.mock_user = Mock()
        self.mock_user.id = 1
        self.mock_user.username = "testuser"

        # Create mock receiver user
        self.mock_receiver = Mock()
        self.mock_receiver.id = 2
        self.mock_receiver.username = "receiver"

        # Create mock conversation
        self.mock_conversation = Mock()
        self.mock_conversation.id = 1
        self.mock_conversation.initiator_id = 1
        self.mock_conversation.receiver_id = 2

        # Create mock message
        self.mock_message = Mock()
        self.mock_message.id = 1
        self.mock_message.content = "Test message"
        self.mock_message.sender_id = 1
        self.mock_message.receiver_id = 2

        # Create mock user public
        self.mock_user_public = Mock()
        self.mock_user_public.id = 2
        self.mock_user_public.username = "receiver"

    @patch('services.conversations.AuthToken.validate')
    @patch('services.conversations.get_conversations_by_user')
    @patch('services.conversations.user_repo.get_users_in_list_by_id')
    def test_get_conversations_success(self, mock_get_users, mock_get_conversations, mock_validate):
        # Arrange
        mock_validate.return_value = self.mock_user

        # Create mock conversations
        mock_conversation1 = Mock()
        mock_conversation1.initiator_id = 1
        mock_conversation1.receiver_id = 2

        mock_conversation2 = Mock()
        mock_conversation2.initiator_id = 3
        mock_conversation2.receiver_id = 1

        mock_get_conversations.return_value = [mock_conversation1, mock_conversation2]
        mock_get_users.return_value = [self.mock_user_public]

        # Act
        result = ConversationsService.get_conversations(self.valid_token)

        # Assert
        self.assertEqual(result, [self.mock_user_public])
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_conversations.assert_called_once_with(self.mock_user.id)
        mock_get_users.assert_called_once_with([2, 3], True)

    @patch('services.conversations.AuthToken.validate')
    def test_get_conversations_invalid_token(self, mock_validate):
        # Arrange
        mock_validate.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ConversationsService.get_conversations(self.invalid_token)

        self.assertEqual(context.exception, invalid_token)
        mock_validate.assert_called_once_with(self.invalid_token)

    @patch('services.conversations.AuthToken.validate')
    @patch('services.conversations.user_repo.get_user_by_id')
    @patch('services.conversations.conversation_exists')
    @patch('services.conversations.create_conversation')
    @patch('services.conversations.create_message')
    def test_send_message_new_conversation(self, mock_create_message, mock_create_conversation,
                                           mock_conversation_exists, mock_get_user, mock_validate):
        # Arrange
        receiver_id = 2
        content = "Test message"
        mock_validate.return_value = self.mock_user
        mock_get_user.return_value = self.mock_receiver
        mock_conversation_exists.return_value = False
        mock_create_conversation.return_value = 1
        mock_create_message.return_value = 1

        # Act
        result = ConversationsService.send_message(receiver_id, content, self.valid_token)

        # Assert
        self.assertEqual(result, {"message_id": 1, "message": "Message sent successfully"})
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_user.assert_called_once_with(receiver_id)
        mock_conversation_exists.assert_called_once_with(self.mock_user.id, receiver_id)
        mock_create_conversation.assert_called_once_with(self.mock_user.id, receiver_id)
        mock_create_message.assert_called_once()

    @patch('services.conversations.AuthToken.validate')
    @patch('services.conversations.user_repo.get_user_by_id')
    @patch('services.conversations.conversation_exists')
    @patch('services.conversations.get_conversation_by_users')
    @patch('services.conversations.create_message')
    def test_send_message_existing_conversation(self, mock_create_message, mock_get_conversation,
                                                mock_conversation_exists, mock_get_user, mock_validate):
        # Arrange
        receiver_id = 2
        content = "Test message"
        mock_validate.return_value = self.mock_user
        mock_get_user.return_value = self.mock_receiver
        mock_conversation_exists.return_value = True
        mock_get_conversation.return_value = 1
        mock_create_message.return_value = 1

        # Act
        result = ConversationsService.send_message(receiver_id, content, self.valid_token)

        # Assert
        self.assertEqual(result, {"message_id": 1, "message": "Message sent successfully"})
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_user.assert_called_once_with(receiver_id)
        mock_conversation_exists.assert_called_once_with(self.mock_user.id, receiver_id)
        mock_get_conversation.assert_called_once_with(self.mock_user.id, receiver_id)
        mock_create_message.assert_called_once()

    @patch('services.conversations.AuthToken.validate')
    def test_send_message_invalid_token(self, mock_validate):
        # Arrange
        receiver_id = 2
        content = "Test message"
        mock_validate.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ConversationsService.send_message(receiver_id, content, self.invalid_token)

        self.assertEqual(context.exception, invalid_token)
        mock_validate.assert_called_once_with(self.invalid_token)

    @patch('services.conversations.AuthToken.validate')
    @patch('services.conversations.user_repo.get_user_by_id')
    def test_send_message_receiver_not_found(self, mock_get_user, mock_validate):
        # Arrange
        receiver_id = 999
        content = "Test message"
        mock_validate.return_value = self.mock_user
        mock_get_user.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ConversationsService.send_message(receiver_id, content, self.valid_token)

        self.assertEqual(context.exception, invalid_credentials)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_user.assert_called_once_with(receiver_id)

    @patch('services.conversations.AuthToken.validate')
    @patch('services.conversations.user_repo.get_user_by_id')
    def test_send_message_to_self(self, mock_get_user, mock_validate):
        # Arrange
        receiver_id = 1  # Same as sender
        content = "Test message"
        mock_validate.return_value = self.mock_user
        mock_get_user.return_value = self.mock_user

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ConversationsService.send_message(receiver_id, content, self.valid_token)

        self.assertEqual(context.exception, invalid_credentials)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_user.assert_called_once_with(receiver_id)

    @patch('services.conversations.AuthToken.validate')
    @patch('services.conversations.get_conversation_by_id')
    @patch('services.conversations.get_messages_by_conversation')
    def test_get_conversation_messages_success(self, mock_get_messages, mock_get_conversation, mock_validate):
        # Arrange
        conversation_id = 1
        mock_validate.return_value = self.mock_user
        mock_get_conversation.return_value = self.mock_conversation
        mock_get_messages.return_value = [self.mock_message]

        # Act
        result = ConversationsService.get_conversation_messages(conversation_id, self.valid_token)

        # Assert
        self.assertEqual(result, [self.mock_message])
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_conversation.assert_called_once_with(conversation_id)
        mock_get_messages.assert_called_once_with(conversation_id)

    @patch('services.conversations.AuthToken.validate')
    def test_get_conversation_messages_invalid_token(self, mock_validate):
        # Arrange
        conversation_id = 1
        mock_validate.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ConversationsService.get_conversation_messages(conversation_id, self.invalid_token)

        self.assertEqual(context.exception, invalid_token)
        mock_validate.assert_called_once_with(self.invalid_token)

    @patch('services.conversations.AuthToken.validate')
    @patch('services.conversations.get_conversation_by_id')
    def test_get_conversation_messages_conversation_not_found(self, mock_get_conversation, mock_validate):
        # Arrange
        conversation_id = 999
        mock_validate.return_value = self.mock_user
        mock_get_conversation.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ConversationsService.get_conversation_messages(conversation_id, self.valid_token)

        self.assertEqual(context.exception, conversation_not_found)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_conversation.assert_called_once_with(conversation_id)

    @patch('services.conversations.AuthToken.validate')
    @patch('services.conversations.get_conversation_by_id')
    def test_get_conversation_messages_user_not_in_conversation(self, mock_get_conversation, mock_validate):
        # Arrange
        conversation_id = 1
        mock_validate.return_value = self.mock_user

        # Create a conversation where the user is not a participant
        mock_conversation = Mock()
        mock_conversation.initiator_id = 3
        mock_conversation.receiver_id = 4

        mock_get_conversation.return_value = mock_conversation

        # Act & Assert
        with self.assertRaises(Exception) as context:
            ConversationsService.get_conversation_messages(conversation_id, self.valid_token)

        self.assertEqual(context.exception, invalid_credentials)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_conversation.assert_called_once_with(conversation_id)


if __name__ == '__main__':
    unittest.main()