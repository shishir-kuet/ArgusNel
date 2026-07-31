import json
import os


class IndexStorage:

    def __init__(self, index_dir="data/index"):

        self.index_dir = index_dir

        # create directory if it doesn't exist
        if not os.path.exists(index_dir):
            os.makedirs(index_dir)

        self.index_file = os.path.join(index_dir, "inverted_index.json")

    def save(self, inverted_index):

        with open(self.index_file, "w", encoding="utf-8") as f:

            json.dump(inverted_index, f, ensure_ascii=False, indent=2)

        print("Index saved to:", self.index_file)

    def load(self):

        if not os.path.exists(self.index_file):

            print("Index file not found")
            return {}

        with open(self.index_file, "r", encoding="utf-8") as f:

            inverted_index = json.load(f)

        return inverted_index