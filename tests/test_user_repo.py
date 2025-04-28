import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from models.auth_model import UserCreate
from models.user import User
from repo.user import get_all_users, get_user_by_id, get_user_by_username, insert_user, gen_user


class TestUserRepo(unittest.TestCase):
    def setUp(self):
        # Sample user data for testing
        self.sample_user_tuple = (
            1,
            "testuser",
            "hashed_password",
            "test@example.com",
            "2023-01-01",
            "avatar.jpg",
            0,
            "2023-01-01"
        )

        self.sample_user = User(
            id=1,
            username="testuser",
            password="hashed_password",
            email="test@example.com",
            birthday="2023-01-01",
            avatar="avatar.jpg",
            admin=0,
            creation_date="2023-01-01"
        )

        self.user_create_data = UserCreate(
            username="newuser",
            password="password123",
            email="new@example.com",
            birthday="2023-01-01"
        )

    def test_gen_user(self):
        # Test the gen_user function
        user = gen_user(self.sample_user_tuple)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

    @patch('repo.user.read_query')
    def test_get_all_users(self, mock_read_query):
        # Mock the read_query function to return sample data
        mock_read_query.return_value = [self.sample_user_tuple]

        # Call the function
        users = get_all_users()

        # Verify the function called read_query with the correct arguments
        mock_read_query.assert_called_once_with("SELECT * FROM users")

        # Verify the result
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, self.sample_user.id)
        self.assertEqual(users[0].username, self.sample_user.username)

    @patch('repo.user.read_query')
    def test_get_user_by_id(self, mock_read_query):
        mock_read_query.return_value = [self.sample_user_tuple]

        user = get_user_by_id(1)

        mock_read_query.assert_called_once_with("SELECT * FROM users WHERE id = ?", (1,))

        self.assertEqual(user.id, self.sample_user.id)
        self.assertEqual(user.username, self.sample_user.username)

    @patch('repo.user.read_query')
    def test_get_user_by_id_not_found(self, mock_read_query):
        mock_read_query.return_value = []

        user = get_user_by_id(999)

        mock_read_query.assert_called_once_with("SELECT * FROM users WHERE id = ?", (999,))

        self.assertIsNone(user)

    @patch('repo.user.read_query')
    def test_get_user_by_username(self, mock_read_query):
        mock_read_query.return_value = [self.sample_user_tuple]

        user = get_user_by_username("testuser")

        mock_read_query.assert_called_once_with("SELECT * FROM users WHERE username = ?", ("testuser",))

        self.assertEqual(user.id, self.sample_user.id)
        self.assertEqual(user.username, self.sample_user.username)

    @patch('repo.user.insert_query')
    def test_insert_user(self, mock_insert_query):
        mock_insert_query.return_value = 5

        result = insert_user(self.user_create_data)

        mock_insert_query.assert_called_once_with(
            "INSERT INTO users (username, password, email, birthday) VALUES (?, ?, ?, ?)",
            (
                self.user_create_data.username,
                self.user_create_data.password,
                self.user_create_data.email,
                self.user_create_data.birthday
            )
        )

        self.assertEqual(result, 5)

    @patch('repo.user.read_query')
    def test_get_all_users_exception(self, mock_read_query):
        mock_read_query.side_effect = Exception("Database error")

        result = get_all_users()

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()