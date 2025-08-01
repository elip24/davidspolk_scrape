from urllib.parse import urljoin
from playwright.async_api import async_playwright
from playwright.sync_api import Playwright, sync_playwright
import asyncio

location_list = ['New York']


def reset_page(page, start_url):
    page.goto(start_url)
    page.wait_for_load_state("networkidle")
    page.locator('button.btn-advance-search').click()
    page.wait_for_load_state("networkidle")


def get_profile_links(playwright, location_list: list[str]):
    browser = playwright.chromium.launch(headless=False)
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    context = browser.new_context(extra_http_headers=custom_headers)
    page = context.new_page()
    page.goto('https://www.davispolk.com/lawyers')
    page.get_by_role('button', name="Office").click()
    label = page.locator("label[for='New York']")
    label.click()


with sync_playwright() as playwright:
    get_profile_links(playwright, location_list=location_list)