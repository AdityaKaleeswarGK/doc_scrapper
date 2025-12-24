import asyncio
from scraper import fetch_html, extract_text_n_link
async def crawl_docs(base_url: str):
    visited = set()
    queue = [base_url]
    with open("text.txt", "a", encoding="utf-8") as f:
        while queue:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)
            print(f"Crawling: {url}")
            try:
                page_html = await fetch_html(url)
                text, links = extract_text_n_link(page_html, url, base_url)
                f.write(text)
                queue.extend(links - visited)
                
            except Exception as e:
                print(f"  Error: {e}")
    
    print(f"Done! Crawled {len(visited)} pages.")

URL = input('Enter the base URL : ')
asyncio.run(crawl_docs(URL))