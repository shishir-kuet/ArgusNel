import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


class WebCrawler:

    def __init__(self, start_url, max_depth=2):
        self.start_url = start_url
        self.max_depth = max_depth
        self.visited = set()
        self.queue = deque([(start_url, 0)])


    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=5)
            return response.text
        except:
            return None


    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")
        links = set()

        for tag in soup.find_all("a", href=True):
            href = tag.get("href")

            if isinstance(href, str):
                link = urljoin(base_url, href)
                parsed = urlparse(link)

                if parsed.scheme in ["http", "https"]:
                    links.add(link)

        return links


    def extract_text(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator=" ", strip=True)


    def crawl(self):

        while self.queue:

            url, depth = self.queue.popleft()

            if url in self.visited or depth > self.max_depth:
                continue

            print(f"Crawling: {url}")

            html = self.fetch_page(url)

            if not html:
                continue

            self.visited.add(url)

            text = self.extract_text(html)

            with open("data/pages.txt", "a", encoding="utf-8") as f:
                f.write(url + "\n")
                f.write(text + "\n\n")

            links = self.extract_links(html, url)

            for link in links:
                self.queue.append((link, depth + 1))