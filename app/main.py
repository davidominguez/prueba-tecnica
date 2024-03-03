from fastapi import FastAPI, UploadFile, File, Query
from schemas.models import Tweet, RssNews
from datetime import date
from typing import List
from controller import get_news_by_criteria, create_new, import_news_from_rss_file, delete_news, get_grouped_news, get_all_news
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()


@app.get("/news/grouped/byProduct")
async def get_news_by_product(start_date: date = Query(None, description="Fecha de inicio en formato YYYY-MM-DD"),
                   end_date: date = Query(None, description="Fecha de fin en formato YYYY-MM-DD")):
    return get_grouped_news(start_date=start_date, end_date=end_date)


@app.get("/news/filter/{product_name}")
async def get_data(product_name: str = None):
    return get_news_by_criteria(products=[product_name])


@app.get("/news")
async def get_news():
    return get_all_news()


@app.post("/news", status_code=201)
async def create_news(news: Tweet | RssNews):
    return create_new(news)


@app.post("/createMassiveNews", status_code=201)
async def create_massive_news(files: List[UploadFile] = File(...)):
    for file in files:
        await import_news_from_rss_file(file)


@app.delete("/deleteAllNews")
async def delete_all_news():
    await delete_news()
