from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class SentimentIndicator(str, Enum):
    POSITIVO = "positivo"
    NEGATIVO = "negativo"
    NEUTRO = "neutro"


class Impact(BaseModel):
    retweets: int = 0
    likes: int = 0
    views: int = 0


class BaseItem(BaseModel):
    title: str
    publication_date: datetime
    government_activity: str
    content: str
    sentiment_indicator: SentimentIndicator = None
    related_products: list[str] = None


class RssNews(BaseItem):
    media: str


class Tweet(BaseItem):
    user: str
    impact: Impact
