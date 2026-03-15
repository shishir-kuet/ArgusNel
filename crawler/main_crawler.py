import requests
import threading
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor


from crawler.url_frontier import URLFrontier
from crawler.url_normalizer import URLNormalizer
from crawler.scheduler import CrawlScheduler
from crawler.robots_handler import RobotsHandler
from crawler.content_deduplicator import ContentDeduplicator
from crawler.page_storage import PageStorage


class MainCrawler:

    def __init__(self, seed_urls):

        self.frontier = URLFrontier()
        self.normalizer = URLNormalizer()
        self.scheduler = CrawlScheduler(delay=0.2)
        self.robots = RobotsHandler()
        self.deduplicator = ContentDeduplicator()
        self.storage = PageStorage()
        self.session = requests.Session()

        # domain crawl control
        self.domain_counts = {}
        self.max_pages_per_domain = 200
        
        self.lock = threading.Lock()
        self.crawled_count = 0

        # Add seed URLs
        for url in seed_urls:
            self.frontier.add_url(url)

    def fetch_page(self, url):

        headers = {
            "User-Agent": "ArgusNelCrawler/1.0 (Educational Project)"
        }

        try:
            response = self.session.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                return None

            content_type = response.headers.get("Content-Type", "")

            # Only process HTML pages
            if "text/html" not in content_type:
                return None

            return response.text

        except Exception as e:
            print("Fetch error:", e)
            return None

    def extract_links(self, html, base_url):

        soup = BeautifulSoup(html, "html.parser")

        links = []

        for tag in soup.find_all("a", href=True):

            href = tag.get("href")

            if not isinstance(href, str):
                continue

            full_url = urljoin(base_url, href)

            links.append(full_url)

        return links

    def extract_text(self, html):

        try:
            soup = BeautifulSoup(html, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)

            return text

        except Exception:
            return ""

    def extract_title(self, html):

        try:
            soup = BeautifulSoup(html, "html.parser")

            if soup.title:
                return soup.title.get_text().strip()

            return "No Title"

        except Exception:
            return "No Title"

    def crawl_worker(self, max_pages):

        while True:

            with self.lock:
                if self.crawled_count >= max_pages:
                    return

            if self.frontier.is_empty():
                time.sleep(0.1)
                continue

            url = self.frontier.get_next_url()

            if not url:
                time.sleep(0.05)
                continue

            url = self.normalizer.normalize(url)

            if not url:
                continue

            domain = urlparse(url).netloc

            # ensure domain count exists and check limit atomically
            with self.lock:
                if domain not in self.domain_counts:
                    self.domain_counts[domain] = 0

                if self.domain_counts[domain] >= self.max_pages_per_domain:
                    # skip URLs from domains that reached their limit
                    continue

            print("\nProcessing:", url)

            if not self.robots.is_allowed(url):
                print("Blocked by robots:", url)
                continue

            self.scheduler.wait_if_needed(url)

            html = self.fetch_page(url)

            if not html:
                continue

            text = self.extract_text(html)

            if not text:
                continue

            if self.deduplicator.is_duplicate(text):
                print("Duplicate skipped")
                continue

            title = self.extract_title(html)

            links = self.extract_links(html, url)

            self.storage.save_page(url, title, text, links)

            # increment domain and global counters atomically
            with self.lock:
                self.domain_counts[domain] += 1
                self.crawled_count += 1

            print("Links found:", len(links))

            for link in links:

                normalized_link = self.normalizer.normalize(link)

                if not normalized_link:
                    continue

                if not normalized_link.startswith("http"):
                    continue

                if normalized_link.endswith((
                ".jpg",".jpeg",".png",".gif",".svg",
                ".pdf",".zip",".rar",
                ".mp4",".mp3",".avi",".mov",
                ".css",".js"
                )):
                    continue

                if any(x in normalized_link for x in ["mailto:", "javascript:", "#"]):
                    continue

                self.frontier.add_url(normalized_link)

            print("Crawled:", url)
            print("Total crawled:", self.crawled_count)
    
    def crawl(self, max_pages=1000, workers=15):

        with ThreadPoolExecutor(max_workers=workers) as executor:

            futures = []

            for _ in range(workers):
                futures.append(executor.submit(self.crawl_worker, max_pages))

            for f in futures:
                f.result()