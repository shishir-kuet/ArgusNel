import os
import json

from indexer.tokenizer import Tokenizer
from indexer.stopwords import StopwordRemover


class IndexBuilder:

    def __init__(self, pages_dir="data/pages"):

        self.pages_dir = pages_dir

        self.tokenizer = Tokenizer()
        self.stopword_remover = StopwordRemover()

        self.inverted_index = {}

    def build(self):

        files = os.listdir(self.pages_dir)

        for filename in files:

            filepath = os.path.join(self.pages_dir, filename)

            with open(filepath, "r", encoding="utf-8") as f:

                data = json.load(f)

            url = data["url"]
            text = data["text"]

            tokens = self.tokenizer.tokenize(text)

            tokens = self.stopword_remover.remove(tokens)

            unique_tokens = set(tokens)

            for token in unique_tokens:

                if token not in self.inverted_index:

                    self.inverted_index[token] = []

                self.inverted_index[token].append(url)

        return self.inverted_index