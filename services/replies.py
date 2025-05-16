from typing import List

from models.reply import Reply
from services.errors import reply_not_found, reply_not_accessible, invalid_token, internal_error, topic_not_found, \
    topic_locked
from services.utils import AuthToken
import repo.replies as replies_repo
import repo.topic as topics_repo
import repo.category as category_repo


class RepliesService:

    # TODO: Not used anywhere
    # @classmethod
    # def get_reply(cls, reply_id: int, token: str) -> Reply:
    #     user = AuthToken.validate(token)
    #     if not user:
    #         raise invalid_token
    #
    #     reply = replies_repo.get_reply_by_id(reply_id)
    #     if not reply:
    #         raise reply_not_found
    #
    #     return reply

    @classmethod
    def set_vote(cls, reply_id: int, vote: int, token: str) -> dict:
        user = AuthToken.validate(token)
        reply = replies_repo.get_reply_by_id(reply_id)
        if not reply:
            raise reply_not_found

        result = replies_repo.set_reply_vote(reply_id, user.id, vote)
        return result

    @classmethod
    def add_reply(cls, content: str, topic_id: int, token: str) -> dict | None:
        user = AuthToken.validate(token)
        topic = topics_repo.get_topic_by_id(topic_id)

        if not topic:
            raise topic_not_found
        if topic.locked == 1:
            raise topic_locked

        if not category_repo.check_category_write_permission(topic.category_id, user) \
                or topic.locked == 1:
            raise reply_not_accessible

        result = replies_repo.add_reply_to_topic(content, topic_id, user.id)
        if not result:
            raise internal_error

        return {"message": "Reply successfully added", "id": result}

    @classmethod
    def set_best_reply(cls, reply_id: int, topic_id: int, token: str) -> bool:
        user = AuthToken.validate(token)
        topic = topics_repo.get_topic_by_id(topic_id)

        if not topic:
            raise topic_not_found

        if topic.user_id != user.id:
            raise reply_not_accessible

        reply = replies_repo.get_reply_by_id(reply_id)
        if not reply:
            raise reply_not_found

        if reply.topic_id != topic_id:
            raise reply_not_accessible

        result = replies_repo.set_reply_as_best(reply_id, topic_id)
        if not result:
            raise internal_error

        return result

    @classmethod
    def get_topic_replies(cls, topic_id, token) -> List[Reply]:
        user = AuthToken.validate(token)
        topic = topics_repo.get_topic_by_id(topic_id)

        if not topic:
            raise topic_not_found

        if not category_repo.check_category_read_permission(topic.category_id, user):
            raise reply_not_accessible

        replies = replies_repo.get_replies_in_topic(topic_id)
        return replies

    @classmethod
    def get_vote(cls, reply_id, token):
        user = AuthToken.validate(token)
        reply = replies_repo.get_reply_by_id(reply_id)
        if not reply:
            raise reply_not_found
        return replies_repo.get_user_vote(reply, user)
