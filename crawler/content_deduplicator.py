import hashlib


class ContentDeduplicator:

    def __init__(self):

        self.content_hashes = set()


    def is_duplicate(self, text):

        content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()

        if content_hash in self.content_hashes:
            return True

        self.content_hashes.add(content_hash)

        return False