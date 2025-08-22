import json
from playwright.sync_api import sync_playwright
from .page_configurations import custom_headers
from .playwright_utils import intercept_route

start_url='https://www.davispolk.com/firm-news/victory-ucla-students-and-faculty-campus-antisemitism-case/'

async def get_each_reference(page,search_reference):
    reference_section = page.locator(f'[data-accordion-title="{search_reference}"]')
    selection_references = reference_section.locator("a.link--internal")
    each_reference = []
    each_text=[]
    count=await selection_references.count()
    for i in range(count):
        text = await  selection_references.nth(i).inner_text()
        href =await  selection_references.nth(i).get_attribute("href")
        each_text.append(text)
        each_reference.append(href)
    return each_text,each_reference

async def extract_article_text(page):
    paragraphs =await page.locator("#article-body-field p").all_inner_texts()
    return "\n\n".join(p.strip() for p in paragraphs)

async def get_news_articles(playwright,browser, start_url):
    context =await browser.new_context(extra_http_headers=custom_headers)
    page = await context.new_page()
    await page.route("**/*", intercept_route)
    await page.goto(start_url)
    data =await page.locator("script[type='application/ld+json']").text_content()
    json_raw=json.loads(data)
    graph=json_raw.get("@graph", [{}])[0]
    headline=graph.get("headline")
    datepublished=graph.get("datePublished")
    capabilities_name,capabilities_link=await get_each_reference(page,search_reference='Related capabilities')
    lawyer_names,lawyer_link=await get_each_reference(page,search_reference='Related lawyers')
    id=await page.get_by_label('Download PDF').get_attribute("href")
    text =await extract_article_text(page)

    all_profile = {
        "id": id,
        "headline": headline,
        "url":start_url,
        "datePublished": datepublished,
        "capabilities":capabilities_name,
        "capabilities_link": capabilities_link,
        "lawyer_names":lawyer_names,
        "lawyer_link": lawyer_link,
        "text": text,
    }
    await page.close()
    await context.close()
    return all_profile