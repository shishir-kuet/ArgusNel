import requests
from urllib.parse import urlparse


class RobotsHandler:

    def __init__(self):
        self.robots_cache = {}


    def fetch_robots(self, url):

        domain = urlparse(url).scheme + "://" + urlparse(url).netloc

        robots_url = domain + "/robots.txt"

        if domain in self.robots_cache:
            return self.robots_cache[domain]

        try:
            response = requests.get(robots_url, timeout=5)

            if response.status_code == 200:
                rules = response.text.splitlines()
                self.robots_cache[domain] = rules
                return rules

        except:
            pass

        self.robots_cache[domain] = []
        return []


    def is_allowed(self, url):

        domain = urlparse(url).scheme + "://" + urlparse(url).netloc
        path = urlparse(url).path

        rules = self.fetch_robots(url)

        for rule in rules:

            if rule.startswith("Disallow:"):

                disallowed_path = rule.split(":")[1].strip()

                if path.startswith(disallowed_path):
                    return False

        return True