import heapq
import threading
from urllib.parse import urlparse


class URLFrontier:

    def __init__(self):

        self.frontier = []
        self.seen_urls = set()

        # thread safety
        self.lock = threading.Lock()


    def add_url(self, url, priority=1):

        with self.lock:

            if url in self.seen_urls:
                return

            heapq.heappush(self.frontier, (priority, url))
            self.seen_urls.add(url)


    def get_next_url(self):

        with self.lock:

            if not self.frontier:
                return None

            priority, url = heapq.heappop(self.frontier)
            return url


    def is_empty(self):

        with self.lock:
            return len(self.frontier) == 0