import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

class TestTopicsRouter(unittest.TestCase):
    def setUp(self):
        self.auth_token = "mocked_token"
        self.topic_id = 1
        self.topic_payload = {
            "name": "Test Topic",
            "content": "This is a test topic.",
            "category_id": 1
        }
        self.mock_topic_response = {
            "id": 1,
            "name": "Test Topic",
            "content": "This is a test topic.",
            "date": "2024-01-01",
            "category_id": 1,
            "category_name": "General",
            "user_id": 1,
            "user_name": "user1",
            "replies_count": 0,
            "locked": 0
        }

    @patch("services.topics.TopicsService.create_topic")
    def test_create_topic(self, mock_create_topic):
        mock_create_topic.return_value = {"topic_id": 1, "message": "Topic created successfully"}
        response = client.post("/topics/", json=self.topic_payload, params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["topic_id"], 1)

    @patch("services.topics.TopicsService.get_topic")
    def test_get_topic(self, mock_get_topic):
        mock_get_topic.return_value = self.mock_topic_response
        response = client.get(f"/topics/{self.topic_id}", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["name"], "Test Topic")

    @patch("services.replies.RepliesService.get_topic_replies")
    def test_get_topic_replies(self, mock_get_topic_replies):
        mock_get_topic_replies.return_value = [
            {"id": 1, "content": "Reply 1", "date": "2024-01-01", "topic_id": 1, "user_id": 2},
            {"id": 2, "content": "Reply 2", "date": "2024-01-02", "topic_id": 1, "user_id": 3}
        ]
        response = client.get(f"/topics/{self.topic_id}/replies", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["content"], "Reply 1")

    @patch("services.topics.TopicsService.get_topics")
    def test_get_topics(self, mock_get_topics):
        mock_get_topics.return_value = [self.mock_topic_response]
        response = client.get("/topics/", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["id"], 1)

    @patch("services.topics.TopicsService.lock_topic_by_id")
    def test_lock_topic(self, mock_lock_topic):
        mock_lock_topic.return_value = True
        response = client.put(f"/topics/{self.topic_id}/lock", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())

if __name__ == "__main__":
    unittest.main()
