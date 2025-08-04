from playwright.async_api import async_playwright

from get_profile_ingestion import get_url_profiles
from news_only import get_news_articles
from profile_only import get_profile_information
from asyncio import Semaphore
import asyncio
from concurrency_utils import process_with_semaphore
import json

from src.ingestion.get_news_ingestion import get_urls_news

MAX_CONCURRENT_REQUESTS = 5
location_list=['New York','Northern California','Washington DC']
start_url_for_queries = "https://dbc8kua830-dsn.algolia.net/1/indexes/*/queries"
start_url="https://www.davispolk.com"

async def main():
    urls_to_scrape=get_url_profiles(start_url_for_queries=start_url_for_queries,
                 start_url=start_url,location_list=location_list)
    async with async_playwright() as playwright:
        semaphore = Semaphore(MAX_CONCURRENT_REQUESTS)
        all_profiles = []
        for url in urls_to_scrape:
            try:
                profile_data = await process_with_semaphore(playwright=playwright,url=url,semaphore=semaphore,
                                                            extractor_function=get_profile_information)
                all_profiles.append(profile_data)
            except Exception as e:
                print(f"Failed to extract {url}: {e}")
                return None
        with open("davidspolk_profile.json", "w", encoding="utf-8") as f:
            json.dump(all_profiles, f, indent=2, ensure_ascii=False)


async def main_news():
    urls_to_scrape=get_urls_news(start_url=start_url)
    async with async_playwright() as playwright:
        semaphore = Semaphore(MAX_CONCURRENT_REQUESTS)
        all_news = []
        for url in urls_to_scrape:
            try:
                news_data = await process_with_semaphore(playwright=playwright,url=url,semaphore=semaphore,
                                                            extractor_function=get_news_articles)
                all_news.append(news_data)
            except Exception as e:
                print(f"Failed to extract {url}: {e}")
                return None
        with open("davidspolk_news.json", "w", encoding="utf-8") as f:
            json.dump(all_news, f, indent=2, ensure_ascii=False)

asyncio.run(main_news())



