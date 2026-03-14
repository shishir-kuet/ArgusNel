from indexer.index_storage import IndexStorage
from search.query_processor import QueryProcessor
from search.ranker import BM25Ranker
import json
import os


class SearchEngine:

    def __init__(self):

        storage = IndexStorage()
        self.index = storage.load()

        self.query_processor = QueryProcessor()
        self.ranker = BM25Ranker(self.index)

        self.pages_dir = "data/pages"

    def get_page_title(self, url):

        for filename in os.listdir(self.pages_dir):

            path = os.path.join(self.pages_dir, filename)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if data["url"] == url:

                text = data["text"]

                # first sentence as title
                title = text.split(".")[0][:120]

                return title

        return "No title"

    def search(self, query, top_k=10):

        tokens = self.query_processor.process(query)

        if not tokens:
            return []

        scores = self.ranker.score(tokens)

        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []

        for doc, score in ranked_docs[:top_k]:

            title = self.get_page_title(doc)

            results.append({
                "url": doc,
                "title": title,
                "score": score
            })

        return results