from playwright.sync_api import sync_playwright
import json
from page_configurations import custom_headers

async def get_capabilities_from_profile(page) -> list[str]:
    capabilities = []
    capability_desk = page.locator("div.lawyer--sidebar-capabilities__desktop div.field-item a")
    count=await capability_desk.count()
    if count > 0:
        capabilities =await capability_desk.all_inner_texts()
    else:
        accordion_caps = page.locator(
            "xpath=//div[normalize-space()='Capabilities']/following::div[contains(@class,'accordion__content')]//a"
        )
        capabilities = await accordion_caps.all_inner_texts()
    return capabilities

async def get_education_from_profile(page)-> list[str]:
    education_heading = page.get_by_role("heading", name="Education")
    education_block = education_heading.locator("xpath=ancestor::div[contains(@class, 'lawyer--education')]")
    degrees =await education_block.locator("div.degree").all_inner_texts()
    return degrees

async def get_profile_information(playwright,start_url):
    browser=await playwright.chromium.launch()
    context=await browser.new_context(extra_http_headers=custom_headers)
    page=await context.new_page()
    await page.goto(start_url)
    data=await page.locator("script[type='application/ld+json']").text_content()
    json_data=json.loads(data)
    graph = json_data.get("@graph", [{}])[0]
    name = graph.get("name")
    url=graph.get("url")
    phone=graph.get("telephone")
    email=graph.get("email")
    location_0 = graph.get("workLocation", {})
    if isinstance(location_0, list):
        location = [loc.get("address", {}).get("addressLocality") for loc in location_0]
    else:
        location = [location_0.get("address", {}).get("addressLocality")]
    capabilities= await get_capabilities_from_profile(page)
    education=await get_education_from_profile(page)
    span_locator = page.get_by_text("Download address card")
    parent_attr = span_locator.locator("xpath=..")
    vcard_href =await parent_attr.get_attribute("href")
    json_data = json.dumps(json_data, ensure_ascii=False)
    all_profile = {
        "name": name,
        "phone": phone,
        "email": email,
        "locations": location,
        "capabilities": capabilities,
        "education": education,
        "vcard_href":vcard_href,
        "url": url,
        "json_data":json_data,
    }
    await page.close()
    await context.close()
    await browser.close()
    return all_profile
