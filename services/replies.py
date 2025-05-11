from models.reply import Reply
from repo.replies import get_reply_by_id, set_reply_vote, add_reply_to_topic, set_reply_as_best
from repo.topic import get_topic_by_id
from services.errors import reply_not_found, reply_not_accessible, invalid_token, internal_error, topic_not_found, \
    reply_invalid_data
from services.utils import AuthToken


class RepliesService:

    @classmethod
    def get_reply(cls, reply_id: int, token: str) -> Reply:
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token

        reply = get_reply_by_id(reply_id)
        if not reply:
            raise reply_not_found

        return reply

    @classmethod
    def set_vote(cls, reply_id: int, vote: int, token: str) -> bool:
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token

        result = set_reply_vote(reply_id, user.id, vote)

        return result

    @classmethod
    def add_reply(cls, content: str, topic_id: int, token: str) -> int | None:
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token

        topic = get_topic_by_id(topic_id)
        if not topic:
            raise topic_not_found

        result = add_reply_to_topic(content, topic_id, user.id)
        if not result:
            raise internal_error

        return result

    @classmethod
    def set_best_reply(cls, reply_id: int, topic_id: int, token: str) -> bool:
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token

        topic = get_topic_by_id(topic_id)
        if not topic:
            raise topic_not_found

        if topic.user_id != user.id:
            raise reply_not_accessible

        reply = get_reply_by_id(reply_id)
        if not reply:
            raise reply_not_found

        if reply.topic_id != topic_id:
            raise reply_not_accessible

        result = set_reply_as_best(reply_id, topic_id)
        if not result:
            raise internal_error

        return result