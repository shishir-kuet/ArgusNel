import math


class BM25Ranker:

    def __init__(self, inverted_index, k1=1.5, b=0.75):

        self.index = inverted_index
        self.k1 = k1
        self.b = b

        # compute document statistics
        self.doc_lengths = {}
        self.avg_doc_length = 0
        self.total_docs = 0

        self._compute_doc_stats()

    def _compute_doc_stats(self):

        total_length = 0

        for term in self.index:

            for doc, freq in self.index[term].items():

                if doc not in self.doc_lengths:
                    self.doc_lengths[doc] = 0

                self.doc_lengths[doc] += freq

        self.total_docs = len(self.doc_lengths)

        if self.total_docs > 0:
            self.avg_doc_length = sum(self.doc_lengths.values()) / self.total_docs

    def score(self, query_tokens):

        scores = {}

        for term in query_tokens:

            if term not in self.index:
                continue

            postings = self.index[term]
            df = len(postings)

            idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1)

            for doc, tf in postings.items():

                doc_len = self.doc_lengths[doc]

                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_length))

                score = idf * (numerator / denominator)

                if doc not in scores:
                    scores[doc] = 0

                scores[doc] += score

        return scores