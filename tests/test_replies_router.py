import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from tests.mock_db import MockConnectionPool


class TestRepliesRouter(unittest.TestCase):
    def setUp(self):
        self.auth_token = "mocked_token"
        self.headers = {"Authorization": self.auth_token}
        self.topic_id = 1
        self.reply_id = 2
        self.mock_reply = {
            "id": 2,
            "content": "Test reply",
            "date": "2024-01-01",
            "topic_id": 1,
            "user_id": 3,
            "best_reply": 0,
            "user_name": "user3",
            "likes": 0
        }

        # Mock the database connection pool
        self.mock_pool = MockConnectionPool()
        self.patcher = patch('data.connection.pool', self.mock_pool)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.client = TestClient(app)

    @patch("services.replies.RepliesService.set_best_reply")
    def test_select_best_reply(self, mock_set_best_reply):
        mock_set_best_reply.return_value = {"success": True}
        response = self.client.put(f"/replies/best/{self.topic_id}/{self.reply_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch("services.replies.RepliesService.set_vote")
    def test_vote_reply(self, mock_set_vote):
        mock_set_vote.return_value = {"vote": 1}
        payload = {"vote_type": 1}
        response = self.client.put(f"/replies/vote/{self.reply_id}", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["vote"], 1)

    @patch("services.replies.RepliesService.get_vote")
    def test_get_user_reply_vote(self, mock_get_vote):
        mock_get_vote.return_value = {"vote": 1}
        response = self.client.get(f"/replies/vote/{self.reply_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["vote"], 1)

    @patch("services.replies.RepliesService.add_reply")
    def test_add_reply(self, mock_add_reply):
        mock_add_reply.return_value = {"message": "Reply successfully added", "id": 2}
        payload = {"content": "Test reply"}
        response = self.client.post(f"/replies/{self.topic_id}", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 2)
        self.assertEqual(response.json()["message"], "Reply successfully added")


if __name__ == "__main__":
    unittest.main()