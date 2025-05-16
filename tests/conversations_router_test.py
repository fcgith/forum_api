import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

class TestConversationsRouter(unittest.TestCase):
    def setUp(self):
        self.auth_token = "mocked_token"

    @patch("services.conversations.ConversationsService.get_conversations")
    def test_get_all_conversations(self, mock_get_conversations):
        mock_get_conversations.return_value = [
            {
                "id": 1,
                "username": "user1",
                "creation_date": "2024-01-01T00:00:00",
                "avatar": None,
                "admin": False,
                "birthday": None,
                "email": "user1@example.com"
            },
            {
                "id": 2,
                "username": "user2",
                "creation_date": "2024-01-02T00:00:00",
                "avatar": None,
                "admin": False,
                "birthday": None,
                "email": "user2@example.com"
            }
        ]
        response = client.get("/conversations/", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["username"], "user1")

    @patch("services.conversations.ConversationsService.get_last_message")
    def test_get_last_message(self, mock_get_last_message):
        mock_get_last_message.return_value = {"id": 1, "content": "Hello!"}
        response = client.get(f"/conversations/last-message/2", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["content"], "Hello!")

    @patch("services.conversations.ConversationsService.send_message")
    def test_send_message(self, mock_send_message):
        mock_send_message.return_value = {"message_id": 1, "message": "Message sent successfully"}
        payload = {"content": "Test message", "receiver_id": 2}
        response = client.post("/conversations/messages/", json=payload, params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Message sent successfully")

    @patch("services.conversations.ConversationsService.get_conversation_messages")
    def test_get_conversation_messages(self, mock_get_conversation_messages):
        mock_get_conversation_messages.return_value = [
            {"id": 1, "content": "Hi"},
            {"id": 2, "content": "Hello"}
        ]
        response = client.get(f"/conversations/1", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["content"], "Hi")

    @patch("services.conversations.ConversationsService.get_messages_between")
    def test_get_messages_between(self, mock_get_messages_between):
        mock_get_messages_between.return_value = [
            {"id": 1, "content": "Message 1"},
            {"id": 2, "content": "Message 2"}
        ]
        response = client.get(f"/conversations/msg/2", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[1]["content"], "Message 2")

if __name__ == "__main__":
    unittest.main()
