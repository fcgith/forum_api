import unittest
from unittest.mock import patch, MagicMock
from services.topics import TopicsService
from services.errors import category_not_found, category_locked, category_not_accessible, topic_not_found, internal_error

class TestTopicsService(unittest.TestCase):
    def setUp(self):
        self.token = "mocked_token"
        self.user = MagicMock(id=1, is_admin=MagicMock(return_value=False))
        self.admin_user = MagicMock(id=99, is_admin=MagicMock(return_value=True))
        self.topic_data = MagicMock(name="Test Topic", content="Test Content", category_id=1)
        self.mock_category = MagicMock(id=1, locked=0)
        self.mock_topic = MagicMock(id=1, category_id=1)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.category_repo.get_category_by_id")
    @patch("services.topics.category_repo.check_category_write_permission")
    @patch("services.topics.topic_repo.create_topic")
    def test_create_topic_success(self, mock_create_topic, mock_check_perm, mock_get_cat, mock_validate):
        mock_validate.return_value = self.user
        mock_get_cat.return_value = self.mock_category
        mock_check_perm.return_value = True
        mock_create_topic.return_value = 42
        result = TopicsService.create_topic(self.topic_data, self.token)
        self.assertEqual(result["topic_id"], 42)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.category_repo.get_category_by_id")
    def test_create_topic_category_not_found(self, mock_get_cat, mock_validate):
        mock_validate.return_value = self.user
        mock_get_cat.return_value = None
        with self.assertRaises(type(category_not_found)):
            TopicsService.create_topic(self.topic_data, self.token)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.category_repo.get_category_by_id")
    def test_create_topic_category_locked(self, mock_get_cat, mock_validate):
        mock_validate.return_value = self.user
        locked_category = MagicMock(id=1, locked=1)
        mock_get_cat.return_value = locked_category
        with self.assertRaises(type(category_locked)):
            TopicsService.create_topic(self.topic_data, self.token)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.category_repo.get_category_by_id")
    @patch("services.topics.category_repo.check_category_write_permission")
    def test_create_topic_no_write_permission(self, mock_check_perm, mock_get_cat, mock_validate):
        mock_validate.return_value = self.user
        mock_get_cat.return_value = self.mock_category
        mock_check_perm.return_value = False
        with self.assertRaises(type(category_not_accessible)):
            TopicsService.create_topic(self.topic_data, self.token)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.category_repo.get_category_by_id")
    @patch("services.topics.category_repo.check_category_write_permission")
    @patch("services.topics.topic_repo.create_topic")
    def test_create_topic_internal_error(self, mock_create_topic, mock_check_perm, mock_get_cat, mock_validate):
        mock_validate.return_value = self.user
        mock_get_cat.return_value = self.mock_category
        mock_check_perm.return_value = True
        mock_create_topic.return_value = None
        with self.assertRaises(type(internal_error)):
            TopicsService.create_topic(self.topic_data, self.token)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.topic_repo.get_topic_by_id")
    @patch("services.topics.category_repo.check_category_read_permission")
    def test_get_topic_success(self, mock_check_read, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.mock_topic
        mock_check_read.return_value = True
        result = TopicsService.get_topic(1, self.token)
        self.assertEqual(result, self.mock_topic)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.topic_repo.get_topic_by_id")
    def test_get_topic_not_found(self, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = None
        with self.assertRaises(type(topic_not_found)):
            TopicsService.get_topic(1, self.token)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.topic_repo.get_topic_by_id")
    @patch("services.topics.category_repo.check_category_read_permission")
    def test_get_topic_no_read_permission(self, mock_check_read, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.mock_topic
        mock_check_read.return_value = False
        self.user.is_admin.return_value = False
        with self.assertRaises(type(category_not_accessible)):
            TopicsService.get_topic(1, self.token)

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.category_repo.get_all_category_ids")
    @patch("services.topics.topic_repo.get_topics")
    def test_get_topics_admin(self, mock_get_topics, mock_get_all_cat_ids, mock_validate):
        mock_validate.return_value = self.admin_user
        mock_get_all_cat_ids.return_value = [1, 2, 3]
        mock_get_topics.return_value = [self.mock_topic]
        result = TopicsService.get_topics(self.token, search=None, page=0, sort="DESC")
        self.assertEqual(result, [self.mock_topic])

    @patch("services.topics.AuthToken.validate")
    @patch("services.topics.category_repo.get_viewable_category_ids")
    @patch("services.topics.topic_repo.get_topics")
    def test_get_topics_non_admin(self, mock_get_topics, mock_get_viewable_cat_ids, mock_validate):
        mock_validate.return_value = self.user
        mock_get_viewable_cat_ids.return_value = [1]
        mock_get_topics.return_value = [self.mock_topic]
        result = TopicsService.get_topics(self.token, search=None, page=0, sort="DESC")
        self.assertEqual(result, [self.mock_topic])

    @patch("services.topics.AuthToken.validate_admin")
    @patch("services.topics.topic_repo.get_topic_by_id")
    @patch("services.topics.topic_repo.lock_topic")
    def test_lock_topic_by_id_success(self, mock_lock_topic, mock_get_topic, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_topic.return_value = self.mock_topic
        mock_lock_topic.return_value = True
        result = TopicsService.lock_topic_by_id(1, self.token)
        self.assertTrue(result)

    @patch("services.topics.AuthToken.validate_admin")
    @patch("services.topics.topic_repo.get_topic_by_id")
    def test_lock_topic_by_id_not_found(self, mock_get_topic, mock_validate_admin):
        mock_validate_admin.return_value = self.admin_user
        mock_get_topic.return_value = None
        with self.assertRaises(type(topic_not_found)):
            TopicsService.lock_topic_by_id(1, self.token)

if __name__ == "__main__":
    unittest.main()
