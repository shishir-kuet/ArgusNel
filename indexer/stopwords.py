class StopwordRemover:

    def __init__(self):

        # Common English stopwords
        self.stopwords = {
            "a", "an", "the", "is", "are", "was", "were",
            "in", "on", "at", "of", "to", "for", "from",
            "and", "or", "but", "if", "then", "than",
            "this", "that", "these", "those",
            "with", "as", "by", "be", "been", "being"
        }

    def remove(self, tokens):

        filtered_tokens = []

        for token in tokens:

            if token not in self.stopwords:
                filtered_tokens.append(token)

        return filtered_tokens