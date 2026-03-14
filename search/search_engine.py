import json
import os

from indexer.index_storage import IndexStorage
from search.query_processor import QueryProcessor
from search.ranker import BM25Ranker
from search.snippet_generator import SnippetGenerator


class SearchEngine:

    def __init__(self):

        storage = IndexStorage()
        self.index = storage.load()

        self.query_processor = QueryProcessor()
        self.ranker = BM25Ranker(self.index)

        self.snippet_generator = SnippetGenerator()

        self.pages_dir = "data/pages"

    def get_page_data(self, url):

        for filename in os.listdir(self.pages_dir):

            path = os.path.join(self.pages_dir, filename)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if data["url"] == url:
                return data

        return None

    def search(self, query, top_k=10):

        tokens = self.query_processor.process(query)

        if not tokens:
            return []

        scores = self.ranker.score(tokens)

        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []

        for doc, score in ranked_docs[:top_k]:

            page = self.get_page_data(doc)

            if not page:
                continue
            
            # Title boost
            title_lower = page["title"].lower()

            for term in tokens:
                if term in title_lower:
                    score += 3

            snippet = self.snippet_generator.generate(page["text"], tokens)

            results.append({
                "title": page["title"],
                "url": doc,
                "snippet": snippet
            })

        return results