import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
import string
import os

class Parse:



    def __init__(self):
        self.stop_words = stopwords.words('english')

        # self.stop_words = set(stopwords.words("english"))
        # add custom words
        # self.stop_words.add('literally') # tell me how
        # self.more_stop_words = ["twitter", "https", "www", "i"]

        self.temp_dict = {} # key: word, value: list of document ids

        self.lowercase_dict = dict.fromkeys(string.ascii_lowercase,"")
        for i in self.lowercase_dict.keys():
            self.lowercase_dict[i] = os.getcwd() + "\\" + i + ".txt"

        self.uppercase_dict = dict.fromkeys(string.ascii_uppercase, "")
        for j in self.uppercase_dict.keys():
            self.uppercase_dict[j] = os.getcwd() + "\\" + j + ".txt"

        self.other_chars = os.getcwd() + "\\" + "other_chars.txt" # will hold file with text beginning in characters that are not letters (numbers, #, $...)

        self.documents = []

    def handle_hashtag(self, hashtag_str:str):
        glue = ' '
        if hashtag_str.__contains__("_"):
            result = hashtag_str.split("_")
        else: # separate by uppercase letters
            result = ''.join(glue + x.lower() if x.isupper() else x for x in hashtag_str).strip(glue).split(glue)

        result.append("#" + hashtag_str.lower().replace("_", ""))

        return result

    def numbers_over_1K(self, num_as_str): # need to deal with "3 million, 4 thousand..."
        k = pow(10,3)
        m = pow(10,6)
        b = pow(10,9)
        num = int(float(num_as_str.replace(",", "")))
        if k <= num < m:
            return str(int(num)/k) + "K"
        if m <= num < b:
            return str(int(num)/m) + "M"
        if num >= b:
            return str(int(num)/b) + "B"

    def handle_tags(self, tag_string):
        return "@" + tag_string

    def upper_or_lower(self, word_to_check):
        if word_to_check[0].isupper():
            return str.upper(word_to_check)
        return word_to_check

    def handle_url(self, url):
        # remove http:\\ ??
        url_split = re.split('://www.([\w\-\.]+)\/', url)
        print(url_split)
        return url_split

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
        new_tokenized_text = []
        # print("\ntokenized text: " + str(tokenized_text))

        doc_length = len(tokenized_text)  # after text operations - length of full_text

        num_dict = {"thousand": "K", "million": "M", "billion": "B", "dollar": "$", "dollars": "$", "percent": "%", "percentage": "%"}


        for i in range(doc_length):
            term = tokenized_text[i]
            next_term = None
            if i + 1 < doc_length:
                next_term = tokenized_text[i+1]
            if term is "@":
                new_tokenized_text.append(self.handle_tags(next_term))
            elif term is "#":
                new_tokenized_text.extend(self.handle_hashtag(next_term))
            elif str.isdigit(term.replace(",", "")): # if term is a number
                num = str(term.replace(",", ""))
                if float(num) > 999:
                    num = self.numbers_over_1K(term)
                if next_term is not None and next_term.lower() in num_dict.keys():
                    new_tokenized_text.append(num + num_dict[next_term])
                else:
                    new_tokenized_text.append(num)
            else:
                new_tokenized_text.append(self.upper_or_lower(term))

        # our rules: numbers? emojis? spelling mistakes? bed.Today?


        print(tokenized_text)
        print(new_tokenized_text)
        print("----")

        for term in new_tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)

        self.documents.append(document)
        Document.update_doc_id()
        return document

    # def add_to_temp_dict(self, doc_as_list):
    #     document = self.parse_doc(doc_as_list)
    #     for word in document.term_doc_dictionary.keys():
    #         letter = word[0]
    #         if letter.isLower():
    #             file = open(self.lowercase_dict[letter],"a")
    #             file.write()




