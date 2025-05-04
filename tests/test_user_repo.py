import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from models.auth_model import UserCreate
from models.user import User, UserPublic
from repo.user import get_all_users, get_user_by_id, get_user_by_username, get_user_by_email, insert_user, gen_user, user_exists, get_users_in_list_by_id


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

        self.sample_user_public = UserPublic(
            id=1,
            username="testuser",
            avatar="avatar.jpg",
            creation_date="2023-01-01"
        )

        self.user_create_data = UserCreate(
            username="newuser",
            password="password123",
            email="new@example.com",
            birthday="2023-01-01"
        )

    def test_gen_user(self):
        # Test the gen_user function with public=False (default)
        user = gen_user(self.sample_user_tuple)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

        # Test the gen_user function with public=True
        user_public = gen_user(self.sample_user_tuple, public=True)
        self.assertEqual(user_public.id, 1)
        self.assertEqual(user_public.username, "testuser")
        self.assertEqual(user_public.avatar, "avatar.jpg")
        # Ensure that email is not present in UserPublic
        self.assertFalse(hasattr(user_public, "email"))

    @patch('repo.user.read_query')
    def test_get_all_users(self, mock_read_query):
        # Mock the read_query function to return sample data
        mock_read_query.return_value = [self.sample_user_tuple]

        # Call the function
        users = get_all_users()

        # Verify the function called read_query
        mock_read_query.assert_called_once()

        # Verify the result
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, self.sample_user.id)
        self.assertEqual(users[0].username, self.sample_user.username)

    @patch('repo.user.read_query')
    def test_get_user_by_id(self, mock_read_query):
        mock_read_query.return_value = [self.sample_user_tuple]

        # Test with public=False (default)
        user = get_user_by_id(1)
        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], (1,))
        self.assertEqual(user.id, self.sample_user.id)
        self.assertEqual(user.username, self.sample_user.username)
        self.assertEqual(user.email, self.sample_user.email)

        # Reset mock for the next test
        mock_read_query.reset_mock()

        # Test with public=True
        user_public = get_user_by_id(1, public=True)
        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], (1,))
        self.assertEqual(user_public.id, self.sample_user_public.id)
        self.assertEqual(user_public.username, self.sample_user_public.username)
        self.assertFalse(hasattr(user_public, "email"))

    @patch('repo.user.read_query')
    def test_get_user_by_id_not_found(self, mock_read_query):
        mock_read_query.return_value = []

        user = get_user_by_id(999)

        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], (999,))

        self.assertIsNone(user)

    @patch('repo.user.read_query')
    def test_get_user_by_username(self, mock_read_query):
        mock_read_query.return_value = [self.sample_user_tuple]

        # Test with public=False (default)
        user = get_user_by_username("testuser")
        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], ("testuser",))
        self.assertEqual(user.id, self.sample_user.id)
        self.assertEqual(user.username, self.sample_user.username)
        self.assertEqual(user.email, self.sample_user.email)

        # Reset mock for the next test
        mock_read_query.reset_mock()

        # Test with public=True
        user_public = get_user_by_username("testuser", public=True)
        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], ("testuser",))
        self.assertEqual(user_public.id, self.sample_user_public.id)
        self.assertEqual(user_public.username, self.sample_user_public.username)
        self.assertFalse(hasattr(user_public, "email"))

    @patch('repo.user.insert_query')
    def test_insert_user(self, mock_insert_query):
        mock_insert_query.return_value = 5

        result = insert_user(self.user_create_data)

        mock_insert_query.assert_called_once()
        # Verify the parameters without checking the SQL query
        self.assertEqual(mock_insert_query.call_args[0][1], (
            self.user_create_data.username,
            self.user_create_data.password,
            self.user_create_data.email,
            self.user_create_data.birthday
        ))

        self.assertEqual(result, 5)

    @patch('repo.user.read_query')
    def test_get_user_by_email(self, mock_read_query):
        mock_read_query.return_value = [self.sample_user_tuple]

        # Test with public=False (default)
        user = get_user_by_email("test@example.com")
        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], ("test@example.com",))
        self.assertEqual(user.id, self.sample_user.id)
        self.assertEqual(user.username, self.sample_user.username)
        self.assertEqual(user.email, self.sample_user.email)

        # Reset mock for the next test
        mock_read_query.reset_mock()

        # Test with public=True
        user_public = get_user_by_email("test@example.com", public=True)
        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], ("test@example.com",))
        self.assertEqual(user_public.id, self.sample_user_public.id)
        self.assertEqual(user_public.username, self.sample_user_public.username)
        self.assertFalse(hasattr(user_public, "email"))

    @patch('repo.user.read_query')
    def test_user_exists(self, mock_read_query):
        # Test when user exists
        mock_read_query.return_value = [self.sample_user_tuple]
        result = user_exists(("testuser", "test@example.com"))
        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], ("testuser", "test@example.com"))
        self.assertTrue(result)

        # Reset mock for the next test
        mock_read_query.reset_mock()

        # Test when user doesn't exist
        mock_read_query.return_value = []
        result = user_exists(("nonexistent", "nonexistent@example.com"))
        mock_read_query.assert_called_once()
        self.assertEqual(mock_read_query.call_args[0][1], ("nonexistent", "nonexistent@example.com"))
        self.assertFalse(result)

    @patch('repo.user.get_user_by_id')
    def test_get_users_in_list_by_id(self, mock_get_user_by_id):
        # Setup mock to return different users for different IDs
        mock_get_user_by_id.side_effect = lambda id, public=False: User(
            id=id,
            username=f"user{id}",
            password="hashed_password",
            email=f"user{id}@example.com",
            birthday="2023-01-01",
            avatar="avatar.jpg",
            admin=0,
            creation_date="2023-01-01"
        ) if not public else UserPublic(
            id=id,
            username=f"user{id}",
            avatar="avatar.jpg",
            creation_date="2023-01-01"
        )

        # Test with public=False (default)
        users = get_users_in_list_by_id([1, 2, 3])
        self.assertEqual(len(users), 3)
        self.assertEqual(users[0].id, 1)
        self.assertEqual(users[0].username, "user1")
        self.assertEqual(users[0].email, "user1@example.com")

        # Test with public=True
        users_public = get_users_in_list_by_id([1, 2, 3], public=True)
        self.assertEqual(len(users_public), 3)
        self.assertEqual(users_public[0].id, 1)
        self.assertEqual(users_public[0].username, "user1")
        self.assertFalse(hasattr(users_public[0], "email"))

    @patch('repo.user.read_query')
    def test_get_all_users_exception(self, mock_read_query):
        mock_read_query.side_effect = Exception("Database error")

        with self.assertRaises(Exception):
            get_all_users()


if __name__ == '__main__':
    unittest.main()
