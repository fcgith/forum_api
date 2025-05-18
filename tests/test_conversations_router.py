import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from tests.mock_db import MockConnectionPool


class TestConversationsRouter(unittest.TestCase):
    def setUp(self):
        self.auth_token = "mocked_token"
        self.headers = {"Authorization": self.auth_token}
        self.mock_user = {
            "id": 1,
            "username": "user1",
            "email": "user1@example.com",
            "password": "hashed_password",
            "birthday": "2000-01-01",
            "creation_date": "2024-01-01",
            "avatar": None,
            "admin": False
        }
        self.mock_message = {
            "id": 1,
            "content": "Hello!",
            "sender_id": 1,
            "receiver_id": 2,
            "date": "2024-01-01T00:00:00",
            "conversation_id": 1
        }

        # Mock the database connection pool
        self.mock_pool = MockConnectionPool()
        self.patcher = patch('data.connection.pool', self.mock_pool)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.client = TestClient(app)

    @patch("services.conversations.ConversationsService.get_conversations")
    def test_get_all_conversations(self, mock_get_conversations):
        mock_get_conversations.return_value = [self.mock_user]
        response = self.client.get("/conversations/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["username"], "user1")

    @patch("services.conversations.ConversationsService.get_last_message")
    def test_get_last_message(self, mock_get_last_message):
        mock_get_last_message.return_value = self.mock_message
        response = self.client.get(f"/conversations/last-message/2", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["content"], "Hello!")

    @patch("services.conversations.ConversationsService.send_message")
    def test_send_message(self, mock_send_message):
        mock_send_message.return_value = {"message_id": 1, "message": "Message sent successfully"}
        payload = {"content": "Test message", "receiver_id": 2}
        response = self.client.post("/conversations/messages/", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Message sent successfully")

    @patch("services.conversations.ConversationsService.get_conversation_messages")
    def test_get_conversation_messages(self, mock_get_conversation_messages):
        mock_get_conversation_messages.return_value = [
            self.mock_message,
            {**self.mock_message, "id": 2, "content": "Hello", "conversation_id": 1}
        ]
        response = self.client.get(f"/conversations/1", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["content"], "Hello!")

    @patch("services.conversations.ConversationsService.get_messages_between")
    def test_get_messages_between(self, mock_get_messages_between):
        mock_get_messages_between.return_value = [
            self.mock_message,
            {**self.mock_message, "id": 2, "content": "Message 2", "conversation_id": 1}
        ]
        response = self.client.get(f"/conversations/msg/2", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[1]["content"], "Message 2")


if __name__ == "__main__":
    unittest.main()
