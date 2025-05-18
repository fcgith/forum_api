import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from tests.mock_db import MockConnectionPool


class TestTopicsRouter(unittest.TestCase):
    def setUp(self):
        self.auth_token = "mocked_token"
        self.headers = {"Authorization": self.auth_token}
        self.topic_id = 1
        self.category_id = 1
        self.mock_topic = {
            "id": 1,
            "name": "Test Topic",
            "content": "Test Content",
            "date": "2024-01-01",
            "category_id": 1,
            "category_name": "Test Category",
            "user_id": 1,
            "user_name": "user1",
            "replies_count": 0,
            "locked": 0
        }
        self.mock_topics_response = {
            "topics": [self.mock_topic],
            "total": 1,
            "page": 0
        }

        # Mock the database connection pool
        self.mock_pool = MockConnectionPool()
        self.patcher = patch('data.connection.pool', self.mock_pool)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.client = TestClient(app)

    @patch("services.topics.TopicsService.get_topics")
    def test_get_all_topics(self, mock_get_topics):
        mock_get_topics.return_value = self.mock_topics_response
        response = self.client.get("/topics/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()["topics"][0]["name"], "Test Topic")

    @patch("services.topics.TopicsService.get_topic")
    def test_get_topic_by_id(self, mock_get_topic):
        mock_get_topic.return_value = self.mock_topic
        response = self.client.get(f"/topics/{self.topic_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["name"], "Test Topic")

    @patch("services.replies.RepliesService.get_topic_replies")
    def test_get_topic_replies(self, mock_get_replies):
        mock_replies = [
            {
                "id": 1,
                "content": "Test Reply",
                "date": "2024-01-01",
                "topic_id": 1,
                "user_id": 1,
                "user_name": "user1",
                "best_reply": False,
                "likes": 0
            }
        ]
        mock_get_replies.return_value = mock_replies
        response = self.client.get(f"/topics/{self.topic_id}/replies", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["content"], "Test Reply")

    @patch("services.topics.TopicsService.create_topic")
    def test_create_topic(self, mock_create_topic):
        mock_create_topic.return_value = {"topic_id": 1, "message": "Topic created successfully"}
        payload = {
            "name": "New Topic",
            "content": "New Content",
            "category_id": 1
        }
        response = self.client.post("/topics/", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["topic_id"], 1)
        self.assertEqual(response.json()["message"], "Topic created successfully")

    @patch("services.topics.TopicsService.lock_topic_by_id")
    def test_lock_topic(self, mock_lock_topic):
        mock_lock_topic.return_value = {"success": True, "message": "Topic locked successfully"}
        response = self.client.put(f"/topics/{self.topic_id}/lock", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["message"], "Topic locked successfully")


if __name__ == "__main__":
    unittest.main()
