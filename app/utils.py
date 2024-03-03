from datetime import date, datetime
from typing import List
from bson.regex import Regex
from schemas.models import Tweet, RssNews, SentimentIndicator
import re
import random
from unidecode import unidecode

from app.data.products import PRODUCTS


def create_date_filters(start_date: date, end_date: date) -> dict:
    # If start_date not exists, get min date
    start_date = datetime.min if start_date is None else start_date

    # If end_date not exists, get today
    end_date = datetime.now() if end_date is None else end_date

    # Append time to date
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())

    # Filter creation
    dates_filter = {
        "publication_date": {
            "$gte": start_datetime,
            "$lte": end_datetime
        }
    }

    return dates_filter


def create_product_filters(product: List[str]) -> dict:
    # TODO: Could be changed to text indexes or another way of searching, since regular expressions are not optimal.
    regex_list = [Regex(keyword, "i") for keyword in product]

    # Filter creation
    product_filter = {
        "$or": [
            {"title": {"$in": regex_list}},
            {"content": {"$in": regex_list}}
        ]
    }

    return product_filter


def create_pipeline_filter_and_group(custom_filter: dict) -> list:

    pipeline = [
        {"$match": custom_filter},
        {
            "$unwind": "$related_products"
        },
        {
            "$group": {
                "_id": "$related_products",
                "news_list": {"$push": "$$ROOT"}
            }
        }
    ]

    return pipeline


def calculate_fields(news: dict) -> RssNews | Tweet:
    '''
        This function mocks the calculation of the sentiment
        of the news item and the products to which it refers.
    '''
    # Get a random value from the enum
    random_value = random.choice(list(SentimentIndicator))
    news["sentiment_indicator"] = random_value

    # Calculate the products referred to in the news item
    # Regular expression to search for each product
    regex_products = '|'.join([re.escape(p) for p in PRODUCTS])
    regex = re.compile(regex_products, re.IGNORECASE)

    # Query to find documents that contain any of the products in the content.
    unicode_lowers_words = unidecode(news["content"].lower())
    matches = regex.findall(unicode_lowers_words)
    news["related_products"] = list(set([element.lower() for element in matches]))

    return news


# Function to parse documents to Tweet or RssNews objects.
def parse_documents_to_news(document) -> Tweet | RssNews:
    # If there is a 'media' key, it is an RssNews object.
    if 'media' in document:
        rss_news = RssNews(**document)
        return rss_news
    # If there is no 'media' key, it is a Tweet object.
    else:
        tweet = Tweet(**document)
        return tweet
