import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from tests.mock_db import MockConnectionPool


class TestCategoryRouter(unittest.TestCase):
    def setUp(self):
        self.auth_token = "mocked_token"
        self.headers = {"Authorization": self.auth_token}
        self.category_id = 1
        self.mock_category = {
            "id": 1,
            "name": "General",
            "description": "General category",
            "hidden": 0,
            "locked": 0,
            "topics_count": 5
        }
        self.mock_topic = {
            "id": 1,
            "name": "Test Topic",
            "content": "Test content",
            "date": "2024-01-01",
            "category_id": 1,
            "category_name": "General",
            "user_id": 1,
            "user_name": "user1",
            "replies_count": 0,
            "locked": 0
        }
        self.mock_user = {
            "id": 1,
            "username": "user1",
            "email": "user1@example.com",
            "password": "hashed_password",
            "birthday": "2000-01-01",
            "creation_date": "2024-01-01"
        }
        self.mock_user_permissions = [
            {"user": self.mock_user, "permission": 3}
        ]

        # Mock the database connection pool
        self.mock_pool = MockConnectionPool()
        self.patcher = patch('data.connection.pool', self.mock_pool)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

        self.client = TestClient(app)

    @patch("services.category.CategoryService.get_all_viewable")
    def test_get_all_categories(self, mock_get_all_viewable):
        mock_get_all_viewable.return_value = [self.mock_category]
        response = self.client.get("/categories/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["name"], "General")

    @patch("services.category.CategoryService.get_by_id")
    def test_get_category_by_id(self, mock_get_by_id):
        mock_get_by_id.return_value = self.mock_category
        response = self.client.get(f"/categories/{self.category_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)

    @patch("services.category.CategoryService.get_topics_by_category_id")
    def test_get_topics_by_category(self, mock_get_topics_by_category_id):
        mock_get_topics_by_category_id.return_value = [self.mock_topic]
        response = self.client.get(f"/categories/{self.category_id}/topics", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["id"], 1)

    @patch("services.category.CategoryService.create")
    def test_create_category(self, mock_create):
        mock_create.return_value = 10
        payload = {"name": "New Category", "description": "A new category"}
        response = self.client.post("/categories/add", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 10)

    @patch("services.category.CategoryService.update_hidden_status")
    def test_update_hide_status(self, mock_update_hidden_status):
        mock_update_hidden_status.return_value = {"success": True, "message": "Category hidden status updated"}
        payload = {"category_id": 1, "hidden": 1}
        response = self.client.put("/categories/hide-status", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch("services.category.CategoryService.update_user_permissions")
    def test_update_user_permissions(self, mock_update_user_permissions):
        mock_update_user_permissions.return_value = {"success": True, "message": "User permissions updated"}
        payload = {"category_id": 1, "user_id": 2, "permission": 3}
        response = self.client.put("/categories/user-permissions", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    @patch("services.user.UserService.get_users_with_permissions_for_category")
    def test_get_users_with_view_or_read_perms(self, mock_get_users_with_perms):
        mock_get_users_with_perms.return_value = self.mock_user_permissions
        response = self.client.get(f"/categories/{self.category_id}/privileged-users", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["user"]["username"], "user1")

    @patch("services.category.CategoryService.get_read_or_write_permission")
    def test_check_authenticated_user_category_permission(self, mock_get_permission):
        mock_get_permission.return_value = "write_access"
        response = self.client.get(f"/categories/{self.category_id}/check-permission", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["access_type"], "write_access")

    @patch("services.category.CategoryService.category_lock")
    def test_lock_category(self, mock_category_lock):
        mock_category_lock.return_value = {"success": True, "message": "Category locked successfully"}
        response = self.client.put(f"/categories/{self.category_id}/lock", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])


if __name__ == "__main__":
    unittest.main()
