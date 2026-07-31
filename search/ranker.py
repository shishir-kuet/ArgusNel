import math
from ranking.pagerank import PageRank


class BM25Ranker:

    def __init__(self, index):

        self.index = index

        self.N = len({doc for term in index for doc in index[term]})

        pagerank = PageRank()
        self.page_ranks = pagerank.compute()

    def score(self, query_terms):

        scores = {}

        for term in query_terms:

            if term not in self.index:
                continue

            docs = self.index[term]

            df = len(docs)

            idf = math.log((self.N - df + 0.5) / (df + 0.5) + 1)

            for doc, tf in docs.items():

                bm25_score = tf * idf

                if doc not in scores:
                    scores[doc] = 0

                scores[doc] += bm25_score
         # Add PageRank influence
        for doc in scores:
            scores[doc] += self.page_ranks.get(doc, 0)        

        # combine pagerank
        for doc in scores:

            scores[doc] += self.page_ranks.get(doc, 0)

        return scores