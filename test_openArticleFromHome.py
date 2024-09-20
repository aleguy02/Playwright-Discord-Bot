import asyncio
from playwright.async_api import Playwright, async_playwright
from bs4 import BeautifulSoup


async def run(playwright: Playwright, url: str) -> None:
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()
    page.set_default_navigation_timeout(60000)
    await page.goto(url, timeout=60000)
    await page.locator("div[class=PagePromo]").locator("span[class=PagePromoContentIcons-text]").first.click()
    await page.wait_for_selector("div.RichTextStoryBody.RichTextBody")

    page_url = (page.url)
    content = await page.content()
    # ---------------------
    await context.close()
    await browser.close()

    return content, page_url

def parse(content: str):
    soup = BeautifulSoup(content, 'lxml')
    headline = soup.select_one('h1[class="Page-headline"]').text

    # parse html to get article contents
    article_p_list = soup.find("div", class_="RichTextStoryBody RichTextBody").find_all("p")

    # combine parsed contents into one string
    article_text = " ".join([p.get_text(" ", strip=True) for p in article_p_list])

    return headline, article_text

async def get_article_data(url: str):
    async with async_playwright() as playwright:
        content, page_url = await run(playwright, url)
        headline, article_text = parse(content)

        return {
            "headline": headline,
            "article": article_text,
            "url": page_url
        }