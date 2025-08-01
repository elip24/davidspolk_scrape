from page_configurations import headers,payload_template
import requests
import json
import time
import copy
import random

def get_url_profiles(start_url_for_queries:str,start_url:str,location_list:list[str]) -> list[str]:
    all_profiles = []
    for location in location_list:
        location_profiles=[]
        print(f"Getting city {location}")
        page = 0

        while True:
            payload = copy.deepcopy(payload_template)
            payload["requests"][0]["facetFilters"] = [[f"office:{location}"]]
            payload["requests"][0]["page"] = page
            try:
                res = requests.post(start_url_for_queries, headers=headers, json=payload)
                res.raise_for_status()
                res_json = res.json()
            except requests.exceptions.RequestException as e:
                break
            hits = res_json['results'][0]['hits']
            if not hits:
                break
            location_profiles.extend(hits)
            print(f"Collecting profiles from page {page}...")
            page += 1
            time.sleep(random.uniform(0.5, 1.5))
        print(f"Total profiles collected from {location}: {len(location_profiles)}")
        all_profiles.extend(location_profiles)

    urls_to_scrape =[f"{start_url}{profile['url']}" for profile in all_profiles if 'url' in profile ]
    urls_to_scrape=list(set(urls_to_scrape))
    return urls_to_scrape