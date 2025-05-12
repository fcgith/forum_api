import unittest
from unittest.mock import Mock, patch

from models.topic import TopicCreate, TopicResponse
from services.topics import TopicsService
from services.errors import invalid_token, category_not_found, category_not_accessible, topic_not_found


class TestTopicsService(unittest.TestCase):
    def setUp(self):
        # Create sample data for testing
        self.valid_token = "valid_token"
        self.invalid_token = "invalid_token"
        self.topic_data = TopicCreate(
            name="Test Topic",
            content="Test Content",
            category_id=1
        )

        # Create mock user
        self.mock_user = Mock()
        self.mock_user.id = 1
        self.mock_user.username = "testuser"
        self.mock_user.is_admin = lambda: False

        # Create mock admin user
        self.mock_admin = Mock()
        self.mock_admin.id = 2
        self.mock_admin.username = "admin"
        self.mock_admin.is_admin = lambda: True

        # Create mock topic
        self.mock_topic = Mock()
        self.mock_topic.id = 1
        self.mock_topic.name = "Test Topic"
        self.mock_topic.content = "Test Content"
        self.mock_topic.category_id = 1
        self.mock_topic.user_id = 1

        # Create mock reply
        self.mock_reply = Mock()
        self.mock_reply.id = 1
        self.mock_reply.content = "Test Reply"
        self.mock_reply.topic_id = 1
        self.mock_reply.user_id = 2

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_category_by_id')
    @patch('services.topics.is_category_viewable')
    @patch('services.topics.create_topic')
    def test_create_topic_success(self, mock_create_topic, mock_is_category_viewable,
                                  mock_get_category_by_id, mock_validate):
        # Arrange
        mock_validate.return_value = self.mock_user
        mock_get_category_by_id.return_value = {"id": 1, "name": "Test Category"}
        mock_is_category_viewable.return_value = True
        mock_create_topic.return_value = 1

        # Act
        result = TopicsService.create_topic(self.topic_data, self.valid_token)

        # Assert
        self.assertEqual(result, {"topic_id": 1, "message": "Topic created successfully"})
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_category_by_id.assert_called_once_with(self.topic_data.category_id)
        mock_is_category_viewable.assert_called_once_with(self.topic_data.category_id, self.mock_user.id)
        mock_create_topic.assert_called_once_with(self.topic_data, self.mock_user.id)

    @patch('services.topics.AuthToken.validate')
    def test_create_topic_invalid_token(self, mock_validate):
        # Arrange
        mock_validate.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            TopicsService.create_topic(self.topic_data, self.invalid_token)

        self.assertEqual(context.exception, invalid_token)
        mock_validate.assert_called_once_with(self.invalid_token)

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_category_by_id')
    def test_create_topic_category_not_found(self, mock_get_category_by_id, mock_validate):
        # Arrange
        mock_validate.return_value = self.mock_user
        mock_get_category_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            TopicsService.create_topic(self.topic_data, self.valid_token)

        self.assertEqual(context.exception, category_not_found)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_category_by_id.assert_called_once_with(self.topic_data.category_id)

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_category_by_id')
    @patch('services.topics.is_category_viewable')
    def test_create_topic_category_not_accessible(self, mock_is_category_viewable,
                                                  mock_get_category_by_id, mock_validate):
        # Arrange
        mock_validate.return_value = self.mock_user
        mock_get_category_by_id.return_value = {"id": 1, "name": "Test Category"}
        mock_is_category_viewable.return_value = False

        # Act & Assert
        with self.assertRaises(Exception) as context:
            TopicsService.create_topic(self.topic_data, self.valid_token)

        self.assertEqual(context.exception, category_not_accessible)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_category_by_id.assert_called_once_with(self.topic_data.category_id)
        mock_is_category_viewable.assert_called_once_with(self.topic_data.category_id, self.mock_user.id)

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_category_by_id')
    @patch('services.topics.is_category_viewable')
    @patch('services.topics.create_topic')
    def test_create_topic_creation_failed(self, mock_create_topic, mock_is_category_viewable,
                                          mock_get_category_by_id, mock_validate):
        # Arrange
        mock_validate.return_value = self.mock_user
        mock_get_category_by_id.return_value = {"id": 1, "name": "Test Category"}
        mock_is_category_viewable.return_value = True
        mock_create_topic.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            TopicsService.create_topic(self.topic_data, self.valid_token)

        self.assertEqual(context.exception, topic_not_found)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_category_by_id.assert_called_once_with(self.topic_data.category_id)
        mock_is_category_viewable.assert_called_once_with(self.topic_data.category_id, self.mock_user.id)
        mock_create_topic.assert_called_once_with(self.topic_data, self.mock_user.id)

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_topic_by_id')
    @patch('services.topics.is_category_viewable')
    @patch('services.topics.get_replies_by_topic_id')
    def test_get_topic_success(self, mock_get_replies, mock_is_category_viewable,
                               mock_get_topic_by_id, mock_validate):
        # Arrange
        topic_id = 1
        mock_validate.return_value = self.mock_user
        mock_get_topic_by_id.return_value = self.mock_topic
        mock_is_category_viewable.return_value = True
        mock_get_replies.return_value = [self.mock_reply]

        # Act
        result = TopicsService.get_topic(topic_id, self.valid_token)

        # Assert
        self.assertEqual(result, {"topic": self.mock_topic, "replies": [self.mock_reply]})
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_topic_by_id.assert_called_once_with(topic_id)
        mock_is_category_viewable.assert_called_once_with(self.mock_topic.category_id, self.mock_user.id)
        mock_get_replies.assert_called_once_with(topic_id)

    @patch('services.topics.AuthToken.validate')
    def test_get_topic_invalid_token(self, mock_validate):
        # Arrange
        topic_id = 1
        mock_validate.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            TopicsService.get_topic(topic_id, self.invalid_token)

        self.assertEqual(context.exception, invalid_token)
        mock_validate.assert_called_once_with(self.invalid_token)

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_topic_by_id')
    def test_get_topic_not_found(self, mock_get_topic_by_id, mock_validate):
        # Arrange
        topic_id = 999
        mock_validate.return_value = self.mock_user
        mock_get_topic_by_id.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            TopicsService.get_topic(topic_id, self.valid_token)

        self.assertEqual(context.exception, topic_not_found)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_topic_by_id.assert_called_once_with(topic_id)

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_topic_by_id')
    @patch('services.topics.is_category_viewable')
    def test_get_topic_category_not_accessible(self, mock_is_category_viewable,
                                               mock_get_topic_by_id, mock_validate):
        # Arrange
        topic_id = 1
        mock_validate.return_value = self.mock_user
        mock_get_topic_by_id.return_value = self.mock_topic
        mock_is_category_viewable.return_value = False

        # Act & Assert
        with self.assertRaises(Exception) as context:
            TopicsService.get_topic(topic_id, self.valid_token)

        self.assertEqual(context.exception, category_not_accessible)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_topic_by_id.assert_called_once_with(topic_id)
        mock_is_category_viewable.assert_called_once_with(self.mock_topic.category_id, self.mock_user.id)

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_all_category_ids')
    @patch('services.topics.get_viewable_category_ids')
    @patch('services.topics.get_topics')
    def test_get_topics_regular_user(self, mock_get_topics, mock_get_viewable_category_ids,
                                     mock_get_all_category_ids, mock_validate):
        # Arrange
        search = "test"
        sort = "name ASC"
        page = 1
        viewable_category_ids = [1, 2, 3]
        expected_topics = [self.mock_topic]

        mock_validate.return_value = self.mock_user
        mock_get_viewable_category_ids.return_value = viewable_category_ids
        mock_get_topics.return_value = expected_topics

        # Act
        result = TopicsService.get_topics(search, sort, page, self.valid_token)

        # Assert
        self.assertEqual(result, expected_topics)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_viewable_category_ids.assert_called_once_with(self.mock_user.id)
        mock_get_all_category_ids.assert_not_called()
        mock_get_topics.assert_called_once_with(search, sort, page, category_ids=viewable_category_ids)

    @patch('services.topics.AuthToken.validate')
    @patch('services.topics.get_all_category_ids')
    @patch('services.topics.get_viewable_category_ids')
    @patch('services.topics.get_topics')
    def test_get_topics_admin_user(self, mock_get_topics, mock_get_viewable_category_ids,
                                   mock_get_all_category_ids, mock_validate):
        # Arrange
        search = "test"
        sort = "name ASC"
        page = 1
        all_category_ids = [1, 2, 3, 4, 5]
        expected_topics = [self.mock_topic]

        mock_validate.return_value = self.mock_admin
        mock_get_all_category_ids.return_value = all_category_ids
        mock_get_topics.return_value = expected_topics

        # Act
        result = TopicsService.get_topics(search, sort, page, self.valid_token)

        # Assert
        self.assertEqual(result, expected_topics)
        mock_validate.assert_called_once_with(self.valid_token)
        mock_get_all_category_ids.assert_called_once()
        mock_get_viewable_category_ids.assert_not_called()
        mock_get_topics.assert_called_once_with(search, sort, page, category_ids=all_category_ids)

    @patch('services.topics.AuthToken.validate')
    def test_get_topics_invalid_token(self, mock_validate):
        # Arrange
        search = "test"
        sort = "name ASC"
        page = 1
        mock_validate.return_value = None

        # Act & Assert
        with self.assertRaises(Exception) as context:
            TopicsService.get_topics(search, sort, page, self.invalid_token)

        self.assertEqual(context.exception, invalid_token)
        mock_validate.assert_called_once_with(self.invalid_token)


if __name__ == '__main__':
    unittest.main()