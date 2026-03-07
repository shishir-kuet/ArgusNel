import json
import os
import hashlib


class PageStorage:

    def __init__(self, storage_dir="data/pages"):

        self.storage_dir = storage_dir

        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)


    def save_page(self, url, text):

        page_id = hashlib.md5(url.encode()).hexdigest()

        page_data = {
            "url": url,
            "text": text
        }

        file_path = os.path.join(self.storage_dir, page_id + ".json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)