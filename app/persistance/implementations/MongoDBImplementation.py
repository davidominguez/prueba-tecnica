import sys
import os
import uuid
from typing import List
from pymongo import MongoClient

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from app.persistance.interfaces.database import IDatabase
from app.schemas.models import Tweet, RssNews
from app.utils import parse_documents_to_news


class MongoDBConnection(IDatabase):
    # TODO:  Singleton pattern
    _instance = None

    def __init__(self, db_name: str, db_user: str, db_password: str):
        assert db_user, "db_url parameter is mandatory"
        assert db_password, "db_password parameter is mandatory"
        assert db_name, "db_name parameter is mandatory"

        # TODO:  Singleton pattern
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        db_url = f"mongodb://{db_user}:{db_password}@mongodb"
        self.client = self.__create_client__(db_url=db_url)
        self.db = self.client[db_name]

    def __create_client__(self, db_url: str):
        try:
            client = MongoClient(db_url)
            return client
        except Exception as e:
            # Error handling but an exception should be thrown indicating that the connection could not be made.
            # TODO: Custom logging...
            raise e

    def create_news(self, news: RssNews | Tweet) -> str:
        insert_result = self.db["news_collection"].insert_one(news.model_dump())
        return insert_result.inserted_id

    def get_news(self, filters: dict = ()) -> List[RssNews | Tweet]:
        documents = list(self.db["news_collection"].find(filters))
        parsed_documents = []
        for document in documents:
            try:
                parsed_doc = parse_documents_to_news(document)
                parsed_documents.append(parsed_doc)
            except Exception as e:
                print(e)
        return parsed_documents

    def get_grouped_news(self, pipeline: list) -> List[RssNews | Tweet]:
        assert pipeline, "pipeline parameter is mandatory"

        result = list(self.db["news_collection"].aggregate(pipeline))

        return result

    def delete_all_news(self):
        self.db["news_collection"].drop()