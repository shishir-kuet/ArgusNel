import time
from urllib.parse import urlparse


class CrawlScheduler:

    def __init__(self, delay:float):
        self.delay = delay
        self.domain_last_access = {}


    def wait_if_needed(self, url):

        domain = urlparse(url).netloc

        last_access = self.domain_last_access.get(domain)

        if last_access:

            elapsed = time.time() - last_access

            if elapsed < self.delay:
                time.sleep(self.delay - elapsed)

        self.domain_last_access[domain] = time.time()