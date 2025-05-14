import repo.topic as topic_repo
import repo.category as category_repo
from models.topic import TopicCreate
from services.errors import invalid_token, category_not_found, category_not_accessible, topic_not_found, internal_error
from services.utils import AuthToken


class TopicsService:
    @classmethod
    def create_topic(cls, data: TopicCreate, token: str):
        """
        Create a new topic

        Args:
            data: Topic data containing name, content, and category_id
            token: Authentication token

        Returns:
            Dictionary with topic ID and status
        """
        user = AuthToken.validate(token)
        category = category_repo.get_category_by_id(data.category_id)

        if not category:
            raise category_not_found

        if not category_repo.check_category_write_permission(data.category_id, user):
            raise category_not_accessible

        topic_id = topic_repo.create_topic(data, user.id)
        if not topic_id:
            raise internal_error

        return {"topic_id": topic_id, "message": "Topic created successfully"}

    @classmethod
    def get_topic(cls, topic_id: int,token: str):
        """
        Get a topic by ID

        Args:
            topic_id: ID of the topic
            token: Authentication token for user validation.

        Returns:
            Topic data
        """
        user = AuthToken.validate(token)
        topic = topic_repo.get_topic_by_id(topic_id)

        if not topic:
            raise topic_not_found
        if not category_repo.check_category_read_permission(topic.category_id, user) and not user.is_admin():
            raise category_not_accessible

        return topic

    @classmethod
    def get_topics(cls, token: str, search:str,page:int=0,sort:str="DESC"):
        """
        Retrieve a list of topics with optional search, sorting, and pagination.

        Args:
            search (str): Optional search keyword to filter topics by name.
            sort (str): Sorting criteria (e.g., "id DESC", "name ASC").
            page (int): Page number for pagination (0-based index).
            token: Authentication token for user validation.

        Returns:
            dict[int, List[Topic]]: A list of Topic objects if found.
        """
        user = AuthToken.validate(token)
        if user.is_admin():
            return topic_repo.get_all_topics()
        topics = topic_repo.get_all_topics()["topics"]

        viewable_category_ids = category_repo.get_viewable_category_ids(user)

        result = topic_repo.get_topics(search=search, sort=sort, page=page, category_ids=viewable_category_ids)
        pages = len(topics) // 10 + 1
        result["pages"] = pages
        return result

    @classmethod
    def lock_topic_by_id(cls, topic_id, token) -> bool:
        ## TODO: add docstring
        AuthToken.validate_admin(token)

        topic = topic_repo.get_topic_by_id(topic_id)
        if not topic:
            raise topic_not_found

        return topic_repo.lock_topic(topic_id)