import unittest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from models.topic import TopicCreate, TopicResponse
from models.user import UserPublic
from routers import topics as topics_router
from services.errors import invalid_token, category_not_found, category_not_accessible, topic_not_found

# Create a mock for the TopicsService
mock_topics_service = Mock(spec='services.topics.TopicsService')

# Replace the actual service with the mock in the router
topics_router.TopicsService = mock_topics_service


def fake_user():
    user = Mock()
    user.id = 1
    user.username = "testuser"
    user.is_admin = lambda: False
    return user


def fake_topic():
    topic = Mock()
    topic.id = 1
    topic.name = "Test Topic"
    topic.content = "Test Content"
    topic.category_id = 1
    topic.user_id = 1
    return topic


def fake_reply():
    reply = Mock()
    reply.id = 1
    reply.content = "Test Reply"
    reply.topic_id = 1
    reply.user_id = 2
    return reply


class TopicsRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        mock_topics_service.reset_mock()

    async def test_createTopic_returnsSuccessResponse_whenTopicIsValid(self):
        # Arrange
        test_token = "valid_token"
        test_topic = TopicCreate(name="Test Topic", content="Test Content", category_id=1)
        expected_response = {"topic_id": 1, "message": "Topic created successfully"}

        mock_topics_service.create_topic.return_value = expected_response

        # Act
        result = await topics_router.create_topic(test_topic, test_token)

        # Assert
        self.assertEqual(expected_response, result)
        mock_topics_service.create_topic.assert_called_once_with(test_topic, test_token)

    async def test_createTopic_raisesException_whenServiceRaisesInvalidToken(self):
        # Arrange
        test_token = "invalid_token"
        test_topic = TopicCreate(name="Test Topic", content="Test Content", category_id=1)

        mock_topics_service.create_topic.side_effect = invalid_token

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await topics_router.create_topic(test_topic, test_token)

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual("Invalid token", context.exception.detail)
        mock_topics_service.create_topic.assert_called_once_with(test_topic, test_token)

    async def test_createTopic_raisesException_whenServiceRaisesCategoryNotFound(self):
        # Arrange
        test_token = "valid_token"
        test_topic = TopicCreate(name="Test Topic", content="Test Content", category_id=999)

        mock_topics_service.create_topic.side_effect = category_not_found

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await topics_router.create_topic(test_topic, test_token)

        self.assertEqual(402, context.exception.status_code)
        self.assertEqual("Category not found", context.exception.detail)
        mock_topics_service.create_topic.assert_called_once_with(test_topic, test_token)

    async def test_createTopic_raisesException_whenServiceRaisesCategoryNotAccessible(self):
        # Arrange
        test_token = "valid_token"
        test_topic = TopicCreate(name="Test Topic", content="Test Content", category_id=1)

        mock_topics_service.create_topic.side_effect = category_not_accessible

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await topics_router.create_topic(test_topic, test_token)

        self.assertEqual(402, context.exception.status_code)
        self.assertEqual("Category not accessible", context.exception.detail)
        mock_topics_service.create_topic.assert_called_once_with(test_topic, test_token)

    async def test_getTopic_returnsTopicAndReplies_whenTopicExists(self):
        # Arrange
        test_token = "valid_token"
        test_topic_id = 1
        test_topic = fake_topic()
        test_replies = [fake_reply()]
        expected_response = {"topic": test_topic, "replies": test_replies}

        mock_topics_service.get_topic.return_value = expected_response

        # Act
        result = await topics_router.get_topic(test_token, test_topic_id)

        # Assert
        self.assertEqual(expected_response, result)
        mock_topics_service.get_topic.assert_called_once_with(test_topic_id, test_token)

    async def test_getTopic_raisesException_whenServiceRaisesInvalidToken(self):
        # Arrange
        test_token = "invalid_token"
        test_topic_id = 1

        mock_topics_service.get_topic.side_effect = invalid_token

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await topics_router.get_topic(test_token, test_topic_id)

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual("Invalid token", context.exception.detail)
        mock_topics_service.get_topic.assert_called_once_with(test_topic_id, test_token)

    async def test_getTopic_raisesException_whenServiceRaisesTopicNotFound(self):
        # Arrange
        test_token = "valid_token"
        test_topic_id = 999

        mock_topics_service.get_topic.side_effect = topic_not_found

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await topics_router.get_topic(test_token, test_topic_id)

        self.assertEqual(402, context.exception.status_code)
        self.assertEqual("Topic not found", context.exception.detail)
        mock_topics_service.get_topic.assert_called_once_with(test_topic_id, test_token)

    async def test_getTopic_raisesException_whenServiceRaisesCategoryNotAccessible(self):
        # Arrange
        test_token = "valid_token"
        test_topic_id = 1

        mock_topics_service.get_topic.side_effect = category_not_accessible

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await topics_router.get_topic(test_token, test_topic_id)

        self.assertEqual(402, context.exception.status_code)
        self.assertEqual("Category not accessible", context.exception.detail)
        mock_topics_service.get_topic.assert_called_once_with(test_topic_id, test_token)

    async def test_getTopics_returnsListOfTopics_whenTokenIsValid(self):
        # Arrange
        test_token = "valid_token"
        test_search = "test"
        test_sort = "name ASC"
        test_page = 1
        expected_topics = [fake_topic()]

        mock_topics_service.get_topics.return_value = expected_topics

        # Act
        result = await topics_router.get_topics(test_token, test_search, test_sort, test_page)

        # Assert
        self.assertEqual(expected_topics, result)
        mock_topics_service.get_topics.assert_called_once_with(test_search, test_sort, test_page, test_token)

    async def test_getTopics_returnsListOfTopics_withDefaultParameters(self):
        # Arrange
        test_token = "valid_token"
        expected_topics = [fake_topic()]

        mock_topics_service.get_topics.return_value = expected_topics

        # Act
        result = await topics_router.get_topics(test_token)

        # Assert
        self.assertEqual(expected_topics, result)
        mock_topics_service.get_topics.assert_called_once_with(None, None, 0, test_token)

    async def test_getTopics_raisesException_whenServiceRaisesInvalidToken(self):
        # Arrange
        test_token = "invalid_token"

        mock_topics_service.get_topics.side_effect = invalid_token

        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            await topics_router.get_topics(test_token)

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual("Invalid token", context.exception.detail)
        mock_topics_service.get_topics.assert_called_once_with(None, None, 0, test_token)


if __name__ == '__main__':
    unittest.main()