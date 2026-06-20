import asyncio
from playwright.async_api import async_playwright

async def parse_url(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        text = await page.evaluate("document.body.innerText")
        title = await page.title()
        await browser.close()
        return {"text": text, "metadata": {"title": title, "page_count": 1}}
