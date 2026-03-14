class Stemmer:

    def stem(self, tokens):

        stemmed = []

        for token in tokens:

            if token.endswith("ing") and len(token) > 4:
                token = token[:-3]

            elif token.endswith("ed") and len(token) > 3:
                token = token[:-2]

            elif token.endswith("es") and len(token) > 3:
                token = token[:-2]

            elif token.endswith("s") and len(token) > 3:
                token = token[:-1]

            stemmed.append(token)

        return stemmed