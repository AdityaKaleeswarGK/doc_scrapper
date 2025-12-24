from playwright.async_api import async_playwright
from lxml import html, etree
from lxml.html.clean import Cleaner
from urllib.parse import urljoin,urlparse
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
def is_useful_link(link: str, current_url: str, base_url: str):
    if not link or link.startswith(('#', 'mailto:', 'tel:', 'javascript:','http://','https://')):
        return None
    full_url = urljoin(current_url, link)
    full_url = full_url.split('#')[0]
    skip_extensions = ('.pdf', '.csv', '.zip', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.mp4', '.mp3')
    if any(full_url.lower().endswith(ext) for ext in skip_extensions):
        return None
    if not full_url.startswith(base_url):
        return None
    
    return full_url  
def extract_text_n_link(page_html:str,current_url:str,base_url:str):
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
    valid_links=set()
    for href in links:
        valid_url = is_useful_link(href, current_url, base_url)
        if valid_url:
            valid_links.add(valid_url)
    print("Extraction done successfully")
    return text_content, valid_links