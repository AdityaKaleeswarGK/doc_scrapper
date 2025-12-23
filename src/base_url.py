import asyncio
from scraper import fetch_html,extract_text_n_link
URL=input('Enter the base URL:')
visited_urls=set()
page_html = asyncio.run(fetch_html(URL))
links=extract_text_n_link(page_html)

