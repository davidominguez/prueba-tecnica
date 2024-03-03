from persistance.implementations.MongoDBImplementation import MongoDBConnection
from typing import List
from datetime import date
from utils import create_date_filters, create_product_filters, calculate_fields, create_pipeline_filter_and_group, parse_documents_to_news
from schemas.models import Tweet, RssNews
from fastapi import File, HTTPException
import feedparser
import datetime
import time
import os


def get_database_connection() -> MongoDBConnection:
    return MongoDBConnection(db_name=os.getenv("MONGO_DB"),
                             db_user=os.getenv("MONGO_USER"),
                             db_password=os.getenv("MONGO_PASS"))


def create_new(news: RssNews | Tweet) -> str:

    # Get database connection
    database = get_database_connection()

    # Calculate sentiment and related products
    news_processed = calculate_fields(news.model_dump())

    # Create object
    parsed = parse_documents_to_news(news_processed)

    # Save in BD
    _id = database.create_news(news=parsed)

    return str(_id)


def get_grouped_news(start_date: date = None, end_date: date = None):

    # Get database connection
    database = get_database_connection()

    # Create dates filters
    date_filter = create_date_filters(start_date, end_date)

    # Create pipeline: filter by dates -> group by products
    pipeline = create_pipeline_filter_and_group(custom_filter=date_filter)

    # DB query
    grouped_news = database.get_grouped_news(pipeline=pipeline)

    # Parse IDs to str
    for news_dict in grouped_news:
        for news in news_dict['news_list']:
            news['_id'] = str(news['_id'])

    return grouped_news


def get_all_news():
    # Get database connection
    database = get_database_connection()

    all_news = database.get_news()

    return all_news


def get_news_by_criteria(products: List[str], start_date: date = None, end_date: date = None) -> List[RssNews | Tweet]:

    # Get database connection
    database = get_database_connection()

    # Dates filters
    date_filter = create_date_filters(start_date, end_date)

    # Product filter
    product_filter = {}
    if products is not None and len(products) != 0:
        product_filter = create_product_filters(products)

    # DB query with filters
    news = database.get_news(filters={**date_filter, **product_filter})

    return news


async def import_news_from_rss_file(file: File):

    # Get database connection
    database = get_database_connection()

    # Check if the uploaded file is an RSS feed
    if not file.filename.endswith(".xml"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an XML file")

    # Read and parse the uploaded file using feedparser
    try:
        content = await file.read()
        parsed_feed = feedparser.parse(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing RSS feed: {str(e)}")

    # Extract relevant data from the parsed feed
    for news in parsed_feed.entries:
        media = news.link
        publication_date = datetime.datetime.fromtimestamp(time.mktime(news.published_parsed))
        if "content" not in news:
            news["content"] = news.summary
        else:
            news["content"] = news.content[0].value
        news_processed = calculate_fields(news)
        rss_news = RssNews(**news_processed, publication_date=publication_date, media=media, government_activity="")
        database.create_news(news=rss_news)


async def delete_news():

    # Get database connection
    database = get_database_connection()

    # DB query
    database.delete_all_news()

