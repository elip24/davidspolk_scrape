import random
from urllib.parse import urljoin

import requests
from .page_configurations import custom_headers
from datetime import datetime, timezone
import time
import json
from bs4 import BeautifulSoup

base_url='https://www.davispolk.com/'

def get_href_and_timestamp_from_api(soup:BeautifulSoup,last_startdate:datetime):
    if last_startdate==None:
        last_startdate = datetime.min.replace(tzinfo=timezone.utc)
    stop_paging=False
    url_for_this_page=[]
    anchors = soup.select(".node-title a")
    time_tag = soup.select(".article--meta time")
    for a, t in zip(anchors, time_tag):
        page_urls = a.get("href", "")
        published_datetime = datetime.fromisoformat(t.get("datetime").replace("Z", "+00:00"))
        if published_datetime >= last_startdate:
            url_for_this_page.append(page_urls)
        else:
            stop_paging=True
            break
    return url_for_this_page, stop_paging


def get_urls_news(start_url:str,last_startdate:datetime) -> list:
    all_news_urls=[]
    page_counter = 0
    while True:
        url = f"https://www.davispolk.com/views/ajax?_wrapper_format=drupal_ajax&view_name=post_landing_page&view_display_id=page_5&view_args=&view_path=%2Fexperience&view_base_path=experience&view_dom_id=4624e145649b07ed95197388a38b99a939c4f526a008b5c86e5b8a7255e9280b&pager_element=0&page={page_counter}&_drupal_ajax=1&ajax_page_state%5Btheme%5D=dpw_2020&ajax_page_state%5Btheme_token%5D=&ajax_page_state%5Blibraries%5D=eJxtkVluwzAMRC8kR0EuJNDSWGVDm4ZIN3FPXyfukrb54fIwGAzIHu5oCddZDSUNLNtqsWJCIwn5jMKuLfFUMHkvms_xYQ5ZG2Jpy0xyoMU16zgLHKHMl3Q6no4xL-Y6dgZB9h9cRXuSznLj2e0_91V4qne-ozhoG5OBWn5Juym_k7NO9qj6TP5MYdB464WchFa0gCVl1TMj3XMzTRnxGUw9NYSqWgXJqca6lb_7gV7p-huOwdhx4YJEgubb7diDreYYY0-G4OustfGwxu8pvDEuFu_1MGpZBDvavjDcDJC2s6nILum-aLfTD3xDth4"
        try:
            print("Reading page ", page_counter)
            res = requests.get(url=url, headers=custom_headers,timeout=10)
            res.raise_for_status()
            response=res.json()
            html = next((item["data"] for item in response if item.get("command") == "insert" and item.get("data")), "")
            soup = BeautifulSoup(html, "html.parser")
            if soup.select(".article--meta"):
                page_urls_rel, stop_paging=get_href_and_timestamp_from_api(soup=soup, last_startdate=last_startdate)
                all_news_urls.extend(page_urls_rel)
                if stop_paging:
                    break
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
