import os
import json
from collections import Counter

from indexer.tokenizer import Tokenizer
from indexer.stopwords import StopwordRemover
from indexer.stemmer import Stemmer


class IndexBuilder:

    def __init__(self, pages_dir="data/pages"):

        self.pages_dir = pages_dir

        self.tokenizer = Tokenizer()
        self.stopword_remover = StopwordRemover()
        self.stemmer = Stemmer()
        self.inverted_index = {}

        # total number of documents
        self.total_docs = 0

    def build(self):

        files = os.listdir(self.pages_dir)

        self.total_docs = len(files)

        for filename in files:

            filepath = os.path.join(self.pages_dir, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            url = data["url"]
            text = data["text"]

            # tokenize text
            tokens = self.tokenizer.tokenize(text)

            # remove stopwords
            tokens = self.stopword_remover.remove(tokens)
            tokens = self.stemmer.stem(tokens)

            # count term frequencies
            term_counts = Counter(tokens)

            for term, freq in term_counts.items():

                if term not in self.inverted_index:
                    self.inverted_index[term] = {}

                self.inverted_index[term][url] = freq

        return self.inverted_index