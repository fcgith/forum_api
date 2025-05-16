import unittest
from unittest.mock import patch, MagicMock
from services.conversations import ConversationsService
from services.errors import not_found, invalid_credentials, conversation_not_found

class TestConversationsService(unittest.TestCase):
    def setUp(self):
        self.token = "mocked_token"
        self.user = MagicMock(id=1)
        self.user2 = MagicMock(id=2)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.user_repo.get_user_by_id")
    @patch("services.conversations.user_repo.get_last_message_between")
    def test_get_last_message_success(self, mock_last_msg, mock_get_user_by_id, mock_validate):
        mock_validate.return_value = self.user
        mock_get_user_by_id.return_value = self.user2
        mock_last_msg.return_value = {"id": 123, "content": "hi"}
        result = ConversationsService.get_last_message(self.user2.id, self.token)
        self.assertEqual(result["id"], 123)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.user_repo.get_user_by_id")
    def test_get_last_message_user_not_found(self, mock_get_user_by_id, mock_validate):
        mock_validate.return_value = self.user
        mock_get_user_by_id.return_value = None
        with self.assertRaises(type(not_found)):
            ConversationsService.get_last_message(self.user2.id, self.token)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.conversation_repo.get_conversations_by_user")
    @patch("services.conversations.user_repo.get_users_in_list_by_id")
    def test_get_conversations(self, mock_get_users, mock_get_convs, mock_validate):
        mock_validate.return_value = self.user
        mock_get_convs.return_value = [
            MagicMock(initiator_id=1, receiver_id=2),
            MagicMock(initiator_id=2, receiver_id=1)
        ]
        mock_get_users.return_value = ["user2"]
        result = ConversationsService.get_conversations(self.token)
        self.assertEqual(result, ["user2"])

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.user_repo.get_user_by_id")
    @patch("services.conversations.conversation_repo.conversation_exists")
    @patch("services.conversations.conversation_repo.create_conversation")
    @patch("services.conversations.conversation_repo.get_conversation_by_users")
    @patch("services.conversations.message_repo.create_message")
    def test_send_message_new_conversation(self, mock_create_msg, mock_get_conv_by_users, mock_create_conv, mock_conv_exists, mock_get_user_by_id, mock_validate):
        mock_validate.return_value = self.user
        mock_get_user_by_id.return_value = self.user2
        mock_conv_exists.return_value = False
        mock_create_conv.return_value = 10
        mock_create_msg.return_value = 99
        mock_get_conv_by_users.return_value = 10
        result = ConversationsService.send_message(self.user2.id, "hello", self.token)
        self.assertEqual(result["message_id"], 99)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.user_repo.get_user_by_id")
    def test_send_message_invalid_receiver(self, mock_get_user_by_id, mock_validate):
        mock_validate.return_value = self.user
        mock_get_user_by_id.return_value = None
        with self.assertRaises(type(invalid_credentials)):
            ConversationsService.send_message(self.user2.id, "hello", self.token)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.conversation_repo.get_conversation_by_id")
    @patch("services.conversations.message_repo.get_messages_by_conversation")
    def test_get_conversation_messages_success(self, mock_get_msgs, mock_get_conv, mock_validate):
        mock_validate.return_value = self.user
        mock_get_conv.return_value = MagicMock(initiator_id=1, receiver_id=2)
        mock_get_msgs.return_value = [{"id": 1, "content": "hi"}]
        result = ConversationsService.get_conversation_messages(5, self.token)
        self.assertEqual(result[0]["id"], 1)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.conversation_repo.get_conversation_by_id")
    def test_get_conversation_messages_not_found(self, mock_get_conv, mock_validate):
        mock_validate.return_value = self.user
        mock_get_conv.return_value = None
        with self.assertRaises(type(conversation_not_found)):
            ConversationsService.get_conversation_messages(5, self.token)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.conversation_repo.get_conversation_by_id")
    def test_get_conversation_messages_invalid_user(self, mock_get_conv, mock_validate):
        mock_validate.return_value = self.user
        mock_get_conv.return_value = MagicMock(initiator_id=3, receiver_id=4)
        with self.assertRaises(type(invalid_credentials)):
            ConversationsService.get_conversation_messages(5, self.token)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.user_repo.get_user_by_id")
    @patch("services.conversations.conversation_repo.get_conversation_between_users")
    @patch("services.conversations.message_repo.get_messages_by_conversation")
    def test_get_messages_between_success(self, mock_get_msgs, mock_get_conv, mock_get_user_by_id, mock_validate):
        mock_validate.return_value = self.user
        mock_get_user_by_id.return_value = self.user2
        mock_get_conv.return_value = MagicMock(id=10)
        mock_get_msgs.return_value = [{"id": 1, "content": "hi"}]
        result = ConversationsService.get_messages_between(self.user2.id, self.token)
        self.assertEqual(result[0]["id"], 1)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.user_repo.get_user_by_id")
    def test_get_messages_between_user_not_found(self, mock_get_user_by_id, mock_validate):
        mock_validate.return_value = self.user
        mock_get_user_by_id.return_value = None
        with self.assertRaises(type(not_found)):
            ConversationsService.get_messages_between(self.user2.id, self.token)

    @patch("services.conversations.AuthToken.validate")
    @patch("services.conversations.user_repo.get_user_by_id")
    @patch("services.conversations.conversation_repo.get_conversation_between_users")
    def test_get_messages_between_conv_not_found(self, mock_get_conv, mock_get_user_by_id, mock_validate):
        mock_validate.return_value = self.user
        mock_get_user_by_id.return_value = self.user2
        mock_get_conv.return_value = None
        with self.assertRaises(type(not_found)):
            ConversationsService.get_messages_between(self.user2.id, self.token)

if __name__ == "__main__":
    unittest.main()
