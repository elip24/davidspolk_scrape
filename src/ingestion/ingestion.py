from playwright.async_api import async_playwright

from .date_functions import get_last_startdate
from .news_only import get_news_articles
from .profile_only import get_profile_information
from asyncio import Semaphore, create_task, gather
import asyncio
from .concurrency_utils import process_with_semaphore
from src.config.settings import client
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


async def main_news(start_url,last_startdate):
    urls_to_scrape = get_urls_news(start_url=start_url,last_startdate=last_startdate)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        semaphore = Semaphore(MAX_CONCURRENT_REQUESTS)
        tasks = [
            create_task(
                process_with_semaphore(
                    playwright=playwright,
                    browser=browser,
                    url=url,
                    semaphore=semaphore,
                    extractor_function=get_news_articles
                )
            )
            for url in urls_to_scrape
        ]
        results = await gather(*tasks, return_exceptions=False)
        all_news = [r for r in results if r is not None]
    await browser.close()
    return all_news


def ingestion():
    last_startdate=get_last_startdate(client)
    all_news=asyncio.run(main_news(start_url,last_startdate))
    return all_news
