import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

class TestUserRouter(unittest.TestCase):
    def setUp(self):
        self.auth_token = "mocked_token"
        self.user_id = 1
        # Full User model for endpoints returning User
        self.mock_user = {
            "id": 1,
            "username": "user1",
            "password": "hashed_password",
            "email": "user1@example.com",
            "birthday": "2000-01-01",
            "avatar": "avatar.jpg",
            "admin": 0,
            "creation_date": "2024-01-01"
        }
        # UserPublic model for endpoints returning UserPublic
        self.mock_user_public = {
            "id": 1,
            "username": "user1",
            "avatar": "avatar.jpg",
            "creation_date": "2024-01-01",
            "admin": 0
        }

    @patch("services.user.UserService.get_users")
    def test_get_all_users(self, mock_get_users):
        mock_get_users.return_value = [self.mock_user]
        response = client.get("/users/", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(response.json()[0]["username"], "user1")
        self.assertIn("password", response.json()[0])
        self.assertIn("email", response.json()[0])
        self.assertIn("birthday", response.json()[0])

    @patch("services.user.UserService.get_user")
    def test_get_user_with_id(self, mock_get_user):
        mock_get_user.return_value = self.mock_user_public
        response = client.get(f"/users/{self.user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["username"], "user1")
        self.assertNotIn("password", response.json())

    @patch("services.user.UserService.get_user_by_username")
    def test_get_by_username(self, mock_get_by_username):
        mock_get_by_username.return_value = self.mock_user_public
        response = client.get(f"/users/search/user1", params={"token": self.auth_token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "user1")
        self.assertNotIn("password", response.json())

    @patch("services.user.UserService.set_avatar")
    def test_update_avatar(self, mock_set_avatar):
        mock_set_avatar.return_value = 1
        payload = {"token": self.auth_token, "link": "avatar.jpg"}
        response = client.put("/users/avatar/", params=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 1)

if __name__ == "__main__":
    unittest.main()
