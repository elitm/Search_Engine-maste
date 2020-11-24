# from nltk.stem import snowball
from nltk.stem import porter


class Stemmer:
    def __init__(self):
        # self.stemmer = snowball.SnowballStemmer("english")
        self.stemmer = porter.PorterStemmer("english")

    def stem_term(self, token):
        """
        This function stem a token
        :param token: string of a token
        :return: stemmed token
        """
        return self.stemmer.stem(token)
