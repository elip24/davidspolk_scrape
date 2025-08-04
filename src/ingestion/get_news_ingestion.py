import random
import requests
from page_configurations import custom_headers
import time
import json
from bs4 import BeautifulSoup

start_url='https://www.davispolk.com'
def get_urls_news(start_url:str) -> list:
    all_news_urls=[]
    page_counter = 0
    while True:
        url = f"https://www.davispolk.com/views/ajax?_wrapper_format=drupal_ajax&view_name=post_landing_page&view_display_id=page_3&view_args=&view_path=%2Fabout%2Fnews&view_base_path=about%2Fnews&view_dom_id=5a8af0aef680fd050b69c6e9523948b09b935ce5a381f8aa3386f7f306752beb&pager_element=0&page={page_counter}&_drupal_ajax=1&ajax_page_state%5Btheme%5D=dpw_2020&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=eJxtkVluwzAMRC8kR0EuJNDSWGVDm4ZIN3FPXyfukrb54fIwGAzIHu5oCddZDSUNLNtqsWJCIwn5jMKuLfFUMHkvms_xYQ5ZG2Jpy0xyoMU16zgLHKHMl3Q6no4xL-Y6dgZB9h9cRXuSznLj2e0_91V4qne-ozhoG5OBWn5Juym_k7NO9qj6TP5MYdB464WchFa0gCVl1TMj3XMzTRnxGUw9NYSqWgXJqca6lb_7gV7p-huOwdhx4YJEgubb7diDreYYY0-G4OustfGwxu8pvDEuFu_1MGpZBDvavjDcDJC2s6nILum-aLfTD3xDth4"
        try:
            print("Reading page ", page_counter)
            res = requests.get(url=url, headers=custom_headers,timeout=10)
            res.raise_for_status()
            response=res.json()
            html = next((item["data"] for item in response if item.get("command") == "insert" and item.get("data")), "")
            soup = BeautifulSoup(html, "html.parser")
            if soup.select("div.article--meta time"):
                dates=[t["datetime"] for t in soup.select("div.article--meta time")]
                urls = [a["href"] for a in soup.select("h4.node-title a")]
                all_news_urls.extend(urls)
                time.sleep(random.uniform(0.5, 1.5))
            else:
                print(f"No more articles on page {page_counter}")
                break
        except requests.exceptions.RequestException as e:
            print(e)
        page_counter += 1

    urls_to_scrape = [f"{start_url}{url}" for url in all_news_urls]
    urls_to_scrape=list(set(urls_to_scrape))
    return urls_to_scrape