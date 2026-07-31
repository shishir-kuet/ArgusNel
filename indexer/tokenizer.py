import re


class Tokenizer:

    def __init__(self):
        pass

    def tokenize(self, text):

        # convert text to lowercase
        text = text.lower()

        # extract words using regex
        tokens = re.findall(r'\b[a-z]+\b', text)

        return tokens