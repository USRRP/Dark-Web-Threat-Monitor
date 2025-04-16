
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import max_pages

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def scrape_site(url):
    visited = set()
    pages_scraped = 0
    collected_html = ""

    def crawl(current_url):
        nonlocal pages_scraped, collected_html
        if current_url in visited or pages_scraped >= max_pages:
            return

        try:
            response = requests.get(current_url, proxies=proxies, headers=headers, timeout=20)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                collected_html += soup.prettify() + "\n\n"
                visited.add(current_url)
                pages_scraped += 1

                for link in soup.find_all("a", href=True):
                    href = link["href"]
                    if href.startswith("/") or url in href:
                        full_url = urljoin(current_url, href)
                        crawl(full_url)

        except Exception as e:
            print(f"Error scraping {current_url}:", e)

    crawl(url)
    return collected_html
