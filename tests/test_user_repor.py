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
            1,  # id
            "testuser",  # username
            "hashed_password",  # password
            "test@example.com",  # email
            "2023-01-01",  # birthday
            "avatar.jpg",  # avatar
            0,  # admin
            "2023-01-01"  # creation_date
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
        # Mock the read_query function to return sample data
        mock_read_query.return_value = [self.sample_user_tuple]

        # Call the function
        user = get_user_by_id(1)

        # Verify the function called read_query with the correct arguments
        mock_read_query.assert_called_once_with("SELECT * FROM users WHERE id = ?", (1,))

        # Verify the result
        self.assertEqual(user.id, self.sample_user.id)
        self.assertEqual(user.username, self.sample_user.username)

    @patch('repo.user.read_query')
    def test_get_user_by_id_not_found(self, mock_read_query):
        # Mock the read_query function to return empty result
        mock_read_query.return_value = []

        # Call the function
        user = get_user_by_id(999)

        # Verify the function called read_query with the correct arguments
        mock_read_query.assert_called_once_with("SELECT * FROM users WHERE id = ?", (999,))

        # Verify the result is None
        self.assertIsNone(user)

    @patch('repo.user.read_query')
    def test_get_user_by_username(self, mock_read_query):
        # Mock the read_query function to return sample data
        mock_read_query.return_value = [self.sample_user_tuple]

        # Call the function
        user = get_user_by_username("testuser")

        # Verify the function called read_query with the correct arguments
        mock_read_query.assert_called_once_with("SELECT * FROM users WHERE username = ?", ("testuser",))

        # Verify the result
        self.assertEqual(user.id, self.sample_user.id)
        self.assertEqual(user.username, self.sample_user.username)

    @patch('repo.user.insert_query')
    def test_insert_user(self, mock_insert_query):
        # Mock the insert_query function to return a user ID
        mock_insert_query.return_value = 5

        # Call the function
        result = insert_user(self.user_create_data)

        # Verify the function called insert_query with the correct arguments
        mock_insert_query.assert_called_once_with(
            "INSERT INTO users (username, password, email, birthday) VALUES (?, ?, ?, ?)",
            (
                self.user_create_data.username,
                self.user_create_data.password,
                self.user_create_data.email,
                self.user_create_data.birthday
            )
        )

        # Verify the result
        self.assertEqual(result, 5)

    @patch('repo.user.read_query')
    def test_get_all_users_exception(self, mock_read_query):
        # Mock the read_query function to raise an exception
        mock_read_query.side_effect = Exception("Database error")

        # Call the function
        result = get_all_users()

        # Verify the result is None
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()