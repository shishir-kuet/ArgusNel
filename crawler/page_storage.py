import os
import json
import hashlib


class PageStorage:

    def __init__(self, storage_dir="data/pages"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)

    def save_page(self, url, title, text, links):

        page_id = hashlib.md5(url.encode()).hexdigest()

        filepath = os.path.join(self.storage_dir, f"{page_id}.json")

        data = {
            "url": url,
            "title": title,
            "text": text,
            "links": links
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)