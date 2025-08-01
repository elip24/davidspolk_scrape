from playwright.sync_api import sync_playwright
import json


start_url='https://www.davispolk.com/lawyers/nausherwan-aamir'

def get_capabilities_from_profile(page) -> list[str]:
    capabilities = []
    capability_desk = page.locator("div.lawyer--sidebar-capabilities__desktop div.field-item a")
    if capability_desk.count() > 0:
        capabilities = capability_desk.all_inner_texts()
    else:
        accordion_caps = page.locator(
            "xpath=//div[normalize-space()='Capabilities']/following::div[contains(@class,'accordion__content')]//a"
        )
        capabilities = accordion_caps.all_inner_texts()
    return capabilities

def get_education_from_profile(page)-> list[str]:
    education_heading = page.get_by_role("heading", name="Education")
    education_block = education_heading.locator("xpath=ancestor::div[contains(@class, 'lawyer--education')]")
    degrees = education_block.locator("div.degree").all_inner_texts()
    return degrees

def get_profile_information(playwright,start_url):
    browser=playwright.chromium.launch(headless=False)
    custom_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    context=browser.new_context(extra_http_headers=custom_headers)
    page=context.new_page()
    page.goto(start_url)
    data=page.locator("script[type='application/ld+json']").text_content()
    json_data=json.loads(data)
    graph = json_data.get("@graph", [{}])[0]
    name = graph.get("name")
    url=graph.get("url")
    phone=graph.get("telephone")
    email=graph.get("email")
    location_0=graph.get("workLocation", {})
    if isinstance(location_0, list):
        location=[loc.get("address",{}).get("addressLocality") for loc in location_0]
    else:
        location=[location_0.get("address", {}).get("addressLocality")]
    capabilities= get_capabilities_from_profile(page)
    education=get_education_from_profile(page)
    span_locator = page.get_by_text("Download address card")
    parent_attr = span_locator.locator("xpath=..")
    vcard_href = parent_attr.get_attribute("href")
    print(location)

with sync_playwright() as playwright:
    get_profile_information(playwright,start_url=start_url)
