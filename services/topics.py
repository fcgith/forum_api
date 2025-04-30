from repo.topic import create_topic, get_topic_by_id, get_topics
# from repo.category import get_category_by_id  # Assuming this exists
from models.topic import TopicCreate, TopicResponse
from services.errors import invalid_token, not_found, category_not_found
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
        # Validate authentication token
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token

        # Validate category exists (assuming get_category_by_id exists)
        # This would be implemented by your teammate working on categories
        # category = get_category_by_id(data.category_id)
        # if not category:
        #     raise category_not_found

        # Create the topic
        topic_id = create_topic(data, user.id)
        if not topic_id:
            raise not_found

        return {"topic_id": topic_id, "message": "Topic created successfully"}

    @classmethod
    def get_topic(cls, topic_id: int,token: str):
        """
        Get a topic by ID

        Args:
            topic_id: ID of the topic

        Returns:
            Topic data
        """
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token
        topic = get_topic_by_id(topic_id)
        if not topic:
            raise not_found

        return topic

    @classmethod
    def get_topics(cls, search:str,sort:str,page:int,token: str):
        """
        Retrieve a list of topics with optional search, sorting, and pagination.

        Args:
            search (str): Optional search keyword to filter topics by name.
            sort (str): Sorting criteria (e.g., "id DESC", "name ASC").
            page (int): Page number for pagination (0-based index).

        Returns:
            List[Topic]: A list of Topic objects if found, otherwise [].
        """
        user = AuthToken.validate(token)
        if not user:
            raise invalid_token
        return get_topics(search,sort,page)