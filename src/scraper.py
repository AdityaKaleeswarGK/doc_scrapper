from playwright.async_api import async_playwright
from lxml import html, etree
from lxml.html.clean import Cleaner
#import requests
async def fetch_html(url: str):
    #html = requests.get(URL).text
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_load_state("networkidle")
        page_html = await page.content()
        await browser.close()
        return page_html

def extract_text_n_link(page_html:str):
    tree = html.fromstring(page_html)
    cleaner = Cleaner(
              scripts=True,
              javascript=True,
              style=True,
              comments=True,
              forms=True,
              annoying_tags=True)
    tree = cleaner.clean_html(tree)
    for tag in ["nav", "header", "footer", "aside","img", "picture", "svg","video", "audio", "canvas"]:
        etree.strip_elements(tree, tag, with_tail=False)
    text_content = " ".join(tree.text_content().split())
    links = tree.xpath("//a/@href")
    with open("text.txt", "a", encoding="utf-8") as f:
        f.write(text_content)
    print("Extraction done successfully")
    return links