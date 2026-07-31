from indexer.tokenizer import Tokenizer
from indexer.stopwords import StopwordRemover
from indexer.stemmer import Stemmer


class QueryProcessor:

    def __init__(self):

        self.tokenizer = Tokenizer()
        self.stopword_remover = StopwordRemover()
        self.stemmer = Stemmer()
    def process(self, query):

        # tokenize query
        tokens = self.tokenizer.tokenize(query)

        # remove stopwords
        tokens = self.stopword_remover.remove(tokens)
        tokens = self.stemmer.stem(tokens)

        return tokens