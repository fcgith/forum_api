import unittest
from unittest.mock import patch, MagicMock
from services.replies import RepliesService
from services.errors import reply_not_found, reply_not_accessible, internal_error, topic_not_found, topic_locked

class TestRepliesService(unittest.TestCase):
    def setUp(self):
        self.token = "mocked_token"
        self.user = MagicMock(id=1)
        self.topic = MagicMock(id=1, category_id=1, locked=0, user_id=1)
        self.reply = MagicMock(id=2, topic_id=1)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.replies_repo.get_reply_by_id")
    @patch("services.replies.replies_repo.set_reply_vote")
    def test_set_vote_success(self, mock_set_vote, mock_get_reply, mock_validate):
        mock_validate.return_value = self.user
        mock_get_reply.return_value = self.reply
        mock_set_vote.return_value = {"vote": 1}
        result = RepliesService.set_vote(2, 1, self.token)
        self.assertEqual(result["vote"], 1)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.replies_repo.get_reply_by_id")
    def test_set_vote_reply_not_found(self, mock_get_reply, mock_validate):
        mock_validate.return_value = self.user
        mock_get_reply.return_value = None
        with self.assertRaises(type(reply_not_found)):
            RepliesService.set_vote(2, 1, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    @patch("services.replies.category_repo.check_category_write_permission")
    @patch("services.replies.replies_repo.add_reply_to_topic")
    def test_add_reply_success(self, mock_add_reply, mock_check_perm, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.topic
        mock_check_perm.return_value = True
        mock_add_reply.return_value = 2
        result = RepliesService.add_reply("Test reply", 1, self.token)
        self.assertEqual(result["id"], 2)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    def test_add_reply_topic_not_found(self, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = None
        with self.assertRaises(type(topic_not_found)):
            RepliesService.add_reply("Test reply", 1, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    def test_add_reply_topic_locked(self, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        locked_topic = MagicMock(id=1, category_id=1, locked=1)
        mock_get_topic.return_value = locked_topic
        with self.assertRaises(type(topic_locked)):
            RepliesService.add_reply("Test reply", 1, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    @patch("services.replies.category_repo.check_category_write_permission")
    def test_add_reply_no_write_permission(self, mock_check_perm, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.topic
        mock_check_perm.return_value = False
        with self.assertRaises(type(reply_not_accessible)):
            RepliesService.add_reply("Test reply", 1, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    @patch("services.replies.category_repo.check_category_write_permission")
    @patch("services.replies.replies_repo.add_reply_to_topic")
    def test_add_reply_internal_error(self, mock_add_reply, mock_check_perm, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.topic
        mock_check_perm.return_value = True
        mock_add_reply.return_value = None
        with self.assertRaises(type(internal_error)):
            RepliesService.add_reply("Test reply", 1, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    @patch("services.replies.replies_repo.get_reply_by_id")
    @patch("services.replies.replies_repo.set_reply_as_best")
    def test_set_best_reply_success(self, mock_set_best, mock_get_reply, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.topic
        self.topic.user_id = self.user.id
        mock_get_reply.return_value = self.reply
        self.reply.topic_id = self.topic.id
        mock_set_best.return_value = True
        result = RepliesService.set_best_reply(self.reply.id, self.topic.id, self.token)
        self.assertTrue(result)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    def test_set_best_reply_topic_not_found(self, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = None
        with self.assertRaises(type(topic_not_found)):
            RepliesService.set_best_reply(self.reply.id, self.topic.id, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    def test_set_best_reply_not_topic_owner(self, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        not_owner_topic = MagicMock(id=1, user_id=99)
        mock_get_topic.return_value = not_owner_topic
        with self.assertRaises(type(reply_not_accessible)):
            RepliesService.set_best_reply(self.reply.id, self.topic.id, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    @patch("services.replies.replies_repo.get_reply_by_id")
    def test_set_best_reply_reply_not_found(self, mock_get_reply, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.topic
        self.topic.user_id = self.user.id
        mock_get_reply.return_value = None
        with self.assertRaises(type(reply_not_found)):
            RepliesService.set_best_reply(self.reply.id, self.topic.id, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    @patch("services.replies.replies_repo.get_reply_by_id")
    def test_set_best_reply_reply_wrong_topic(self, mock_get_reply, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.topic
        self.topic.user_id = self.user.id
        wrong_reply = MagicMock(id=2, topic_id=99)
        mock_get_reply.return_value = wrong_reply
        with self.assertRaises(type(reply_not_accessible)):
            RepliesService.set_best_reply(self.reply.id, self.topic.id, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    @patch("services.replies.category_repo.check_category_read_permission")
    @patch("services.replies.replies_repo.get_replies_in_topic")
    def test_get_topic_replies_success(self, mock_get_replies, mock_check_perm, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.topic
        mock_check_perm.return_value = True
        mock_get_replies.return_value = [self.reply]
        result = RepliesService.get_topic_replies(self.topic.id, self.token)
        self.assertEqual(result, [self.reply])

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    def test_get_topic_replies_topic_not_found(self, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = None
        with self.assertRaises(type(topic_not_found)):
            RepliesService.get_topic_replies(self.topic.id, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.topics_repo.get_topic_by_id")
    @patch("services.replies.category_repo.check_category_read_permission")
    def test_get_topic_replies_no_permission(self, mock_check_perm, mock_get_topic, mock_validate):
        mock_validate.return_value = self.user
        mock_get_topic.return_value = self.topic
        mock_check_perm.return_value = False
        with self.assertRaises(type(reply_not_accessible)):
            RepliesService.get_topic_replies(self.topic.id, self.token)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.replies_repo.get_reply_by_id")
    @patch("services.replies.replies_repo.get_user_vote")
    def test_get_vote_success(self, mock_get_user_vote, mock_get_reply, mock_validate):
        mock_validate.return_value = self.user
        mock_get_reply.return_value = self.reply
        mock_get_user_vote.return_value = {"vote": 1}
        result = RepliesService.get_vote(self.reply.id, self.token)
        self.assertEqual(result["vote"], 1)

    @patch("services.replies.AuthToken.validate")
    @patch("services.replies.replies_repo.get_reply_by_id")
    def test_get_vote_reply_not_found(self, mock_get_reply, mock_validate):
        mock_validate.return_value = self.user
        mock_get_reply.return_value = None
        with self.assertRaises(type(reply_not_found)):
            RepliesService.get_vote(self.reply.id, self.token)

if __name__ == "__main__":
    unittest.main()
