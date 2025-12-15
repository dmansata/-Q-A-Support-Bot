import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

class Crawler:
    def __init__(self):
        self.visited = set()
        self.pages = []

    def is_valid_url(self, url, base_domain):
        parsed = urlparse(url)
        return parsed.netloc == base_domain and parsed.scheme in ['http', 'https']

    def is_wanted_page(self, url):
        # Skip common unwanted pages
        unwanted = ['login', 'signup', 'cart', 'checkout', 'javascript:', 'mailto:']
        return not any(x in url.lower() for x in unwanted)

    def crawl(self, start_url, max_pages=10, max_depth=2):
        self.visited = set()
        self.pages = []
        base_domain = urlparse(start_url).netloc
        queue = [(start_url, 0)]
        self.visited.add(start_url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        while queue and len(self.pages) < max_pages:
            url, depth = queue.pop(0)

            if depth > max_depth:
                continue

            try:
                print(f"Crawling: {url}")
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.title.string if soup.title else url
                    
                    self.pages.append({
                        "url": url,
                        "title": title,
                        "html": response.text
                    })

                    if depth < max_depth:
                        for link in soup.find_all('a', href=True):
                            next_url = urljoin(url, link['href'])
                            if (self.is_valid_url(next_url, base_domain) and 
                                self.is_wanted_page(next_url) and 
                                next_url not in self.visited):
                                self.visited.add(next_url)
                                queue.append((next_url, depth + 1))
                time.sleep(1) # Be polite
            except Exception as e:
                print(f"Error crawling {url}: {e}")

        return self.pages
