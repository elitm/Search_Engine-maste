from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import string
import os


class Parse:



    def __init__(self):
        # self.stop_words = stopwords.words('english')

        self.stop_words = set(stopwords.words("english"))
        # add custom words
        self.stop_words.add('literally') # tell me how

        self.temp_dict = {} # key: word, value: list of document ids

        self.lowercase_dict = dict.fromkeys(string.ascii_lowercase,"")
        for i in self.lowercase_dict.keys():
            self.lowercase_dict[i] = os.getcwd() + "\\" + i + ".txt"

        self.uppercase_dict = dict.fromkeys(string.ascii_uppercase, "")
        for j in self.uppercase_dict.keys():
            self.uppercase_dict[j] = os.getcwd() + "\\" + j + ".txt"

        self.other_chars = os.getcwd() + "\\" + "other_chars.txt" # will hold file with text beginning in characters that are not letters (numbers, #, $...)

        self.documents = []





    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """

        text_tokens = word_tokenize(text)
        # text_lower_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        text_tokens_without_stopwords = [w for w in text_tokens if w not in self.stop_words]
        # print(text_tokens_without_stopwords)
        return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """

        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)

        doc_length = len(tokenized_text)  # after text operations - length of full_text

        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        # print("\n" + document)
        print("\n\ntokenized text: " + str(tokenized_text))

        self.documents.append(document)
        Document.update_doc_id()

        return document

    def add_to_temp_dict(self, doc_as_list):
        document = self.parse_doc(doc_as_list)
        for word in document.term_doc_dictionary.keys():
            letter = word[0]
            if letter.isLower():
                file = open(self.lowercase_dict[letter],"a")
                file.write()




