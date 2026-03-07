import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from crawler.url_frontier import URLFrontier
from crawler.url_normalizer import URLNormalizer
from crawler.scheduler import CrawlScheduler
from crawler.robots_handler import RobotsHandler
from crawler.content_deduplicator import ContentDeduplicator
from crawler.page_storage import PageStorage


class MainCrawler:

    def __init__(self, start_url):

        self.frontier = URLFrontier()
        self.normalizer = URLNormalizer()
        self.scheduler = CrawlScheduler(delay=1)
        self.robots = RobotsHandler()
        self.deduplicator = ContentDeduplicator()
        self.storage = PageStorage()

        # store allowed domain
        self.allowed_domain = urlparse(start_url).netloc

        self.frontier.add_url(start_url)

    def fetch_page(self, url):

        headers = {
            "User-Agent": "ArgusNelCrawler/1.0 (Educational Project)"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                return response.text
            else:
                print("HTTP Error:", response.status_code)

        except Exception as e:
            print("Fetch error:", e)

        return None

    def extract_links(self, html, base_url):

        soup = BeautifulSoup(html, "html.parser")

        links = []

        for tag in soup.find_all("a", href=True):

            href = tag.get("href")

            if isinstance(href, str):

                full_url = urljoin(base_url, href)

                links.append(full_url)

        return links

    def extract_text(self, html):

        soup = BeautifulSoup(html, "html.parser")

        return soup.get_text(separator=" ", strip=True)

    def crawl(self, max_pages=50):

        crawled = 0

        while not self.frontier.is_empty() and crawled < max_pages:

            url = self.frontier.get_next_url()

            if not url:
                break

            url = self.normalizer.normalize(url)

            print("\nProcessing:", url)

            # domain restriction
            if urlparse(url).netloc != self.allowed_domain:
                print("Skipping external domain:", url)
                continue

            if not self.robots.is_allowed(url):
                print("Blocked by robots:", url)
                continue

            self.scheduler.wait_if_needed(url)

            html = self.fetch_page(url)

            if not html:
                print("Failed to fetch:", url)
                continue

            text = self.extract_text(html)

            if self.deduplicator.is_duplicate(text):
                print("Duplicate page skipped")
                continue

            self.storage.save_page(url, text)

            links = self.extract_links(html, url)

            print("Links found:", len(links))

            for link in links:

                normalized_link = self.normalizer.normalize(link)

                self.frontier.add_url(normalized_link)

            crawled += 1

            print("Crawled:", url)