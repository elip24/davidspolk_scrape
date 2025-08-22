import json
from playwright.sync_api import sync_playwright
from src.ingestion.page_configurations import custom_headers

start_url='https://www.davispolk.com/firm-news/victory-ucla-students-and-faculty-campus-antisemitism-case/'

def get_each_reference(page,search_reference):
    reference_section = page.locator(f'[data-accordion-title="{search_reference}"]')
    selection_references = reference_section.locator("a.link--internal")
    each_reference = []
    count=selection_references.count()
    for i in range(count):
        href = selection_references.nth(i).get_attribute("href")
        each_reference.append(href)
    return each_reference

def extract_article_text(page):
    paragraphs =page.locator("#article-body-field p").all_inner_texts()
    return "\n\n".join(p.strip() for p in paragraphs)

def get_news_articles(playwright, start_url):
    browser =playwright.chromium.launch()
    context =browser.new_context(extra_http_headers=custom_headers)
    page = context.new_page()
    page.goto(start_url)
    data =page.locator("script[type='application/ld+json']").text_content()
    json_raw=json.loads(data)
    graph=json_raw.get("@graph", [{}])[0]
    headline=graph.get("headline")
    datePublished=graph.get("datePublished")
    capabilities_link=get_each_reference(page,search_reference='Related capabilities')
    lawyers_link=get_each_reference(page,search_reference='Related lawyers')
    id=page.get_by_label('Download PDF').get_attribute("href")
    text =extract_article_text(page)

    all_profile = {
        "headline": headline,
        "url":start_url,
        "datePublished": datePublished,
        "capabilities_link": capabilities_link,
        "lawyers_link": lawyers_link,
        "id": id,
        "text": text,
        "json_raw": json_raw
    }
    return all_profile



with sync_playwright() as p:
    get_news_articles(p,start_url=start_url)