class SnippetGenerator:

    def generate(self, text, query_terms):

        sentences = text.split(".")

        for sentence in sentences:

            lower = sentence.lower()

            for term in query_terms:

                if term in lower:

                    return sentence.strip()[:200]

        return text[:200]