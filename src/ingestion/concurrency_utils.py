from asyncio import Semaphore

async def process_with_semaphore(playwright, url: str, semaphore: Semaphore, extractor_function) -> dict:
    async with semaphore:
        print(f"Processing: {url}")
        try:
            data = await extractor_function(playwright, url)
            return data
        except Exception as e:
            print(f" Exception: {e}")
            return None
