custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
}

#The headers directly from their site
headers = {
    "x-algolia-agent": "Algolia for JavaScript (5.34.0); Lite (5.34.0); Browser; instantsearch.js (4.79.1); JS Helper (3.26.0)",
    "x-algolia-api-key": "8fa5ef586d1836ee07daf12366932e8c",
    "x-algolia-application-id": "DBC8KUA830",
    "Content-Type": "application/json"
}
payload_template = {
    "requests": [
        {
            "indexName": "lawyer_search_en",
            "clickAnalytics": True,
            "facetFilters": [[]], #inside the two brackets it goes the location filter this way: "office:New York"
            "facets": [
                "clerkship", "industry", "job_title", "language",
                "office", "practice", "region", "school"
            ],
            "highlightPostTag": "__/ais-highlight__",
            "highlightPreTag": "__ais-highlight__",
            "maxValuesPerFacet": 1000,
            "page": 0,
            "query": ""
        }
    ]
}

