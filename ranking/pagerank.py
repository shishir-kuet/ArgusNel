import os
import json
from collections import defaultdict


class PageRank:

    def __init__(self, pages_dir="data/pages", damping=0.85, iterations=20):

        self.pages_dir = pages_dir
        self.damping = damping
        self.iterations = iterations

    def build_graph(self):

        graph = defaultdict(set)

        for filename in os.listdir(self.pages_dir):

            path = os.path.join(self.pages_dir, filename)

            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            url = data["url"]

            if "links" in data:
                for link in data["links"]:
                    graph[url].add(link)

        return graph

    def compute(self):

        graph = self.build_graph()

        pages = list(graph.keys())

        N = len(pages)

        ranks = {page: 1 / N for page in pages}

        for _ in range(self.iterations):

            new_ranks = {}

            for page in pages:

                rank_sum = 0

                for other_page in pages:

                    if page in graph[other_page]:

                        rank_sum += ranks[other_page] / len(graph[other_page])

                new_ranks[page] = (1 - self.damping) / N + self.damping * rank_sum

            ranks = new_ranks

        return ranks