from abc import abstractmethod
from app.schemas.models import Tweet, RssNews
from typing import List


class IDatabase:
    _instance = None

    @abstractmethod
    def __init__(self, db_name: str, db_user: str, db_password: str):
        pass

    @abstractmethod
    def __create_client__(self, db_url: str):
        pass

    @abstractmethod
    def create_news(self, news: RssNews | Tweet) -> str:
        pass

    @abstractmethod
    def get_news(self, filters: dict = ()) -> List[RssNews | Tweet]:
        pass

    @abstractmethod
    def get_grouped_news(self, pipeline: list) -> List[RssNews | Tweet]:
        pass

    @abstractmethod
    def delete_all_news(self):
        pass
