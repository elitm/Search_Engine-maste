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

        self.temp_dict = {}  # key: word, value: list of document ids

        self.lowercase_dict = dict.fromkeys(string.ascii_lowercase, "")
        for i in self.lowercase_dict.keys():
            self.lowercase_dict[i] = os.getcwd() + "\\" + i + ".txt"

        self.uppercase_dict = dict.fromkeys(string.ascii_uppercase, "")
        for j in self.uppercase_dict.keys():
            self.uppercase_dict[j] = os.getcwd() + "\\" + j + ".txt"

        self.other_chars = os.getcwd() + "\\" + "other_chars.txt"  # will hold file with text beginning in characters that are not letters (numbers, #, $...)

        self.documents = []


    def handle_hashtag(self, hashtag_str: str):
        glue = ' '
        if hashtag_str.__contains__("_"):
            result = hashtag_str.split("_")
        else:  # separate by uppercase letters
            result = ''.join(glue + x.lower() if x.isupper() else x for x in hashtag_str).strip(glue).split(glue)
        result.append("#" + hashtag_str.lower().replace("_", ""))

        return result

    def numbers_over_1K(self, num_as_str):
        k = pow(10, 3)
        m = pow(10, 6)
        b = pow(10, 9)
        num = int(float(num_as_str.replace(",", "")))
        if k <= num < m:
            return str(int(num) / k) + "K"
        if m <= num < b:
            return str(int(num) / m) + "M"
        if num >= b:
            return str(int(num) / b) + "B"


    def handle_tags(self, tag_string):
        return "@" + tag_string

    def upper_or_lower(self, word_to_check):
        if word_to_check[0].isupper():
            return str.upper(word_to_check)
        return word_to_check

    def handle_url(self, url_token:str):
        # url_token.replace("https", "")
        url_token = url_token[8:]
        split_url = []
        space_or_char = ""

        delimiters = {"=", "?", "/", ":"}

        for char in url_token:
            if char in delimiters and space_or_char != "":
                split_url.append(space_or_char)
                space_or_char = ""
            else:
                space_or_char += char
        split_url.append(space_or_char)
        # split_url.remove("/")
        return split_url

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """
        with open('stop_words.txt', 'r') as f:
            lines = f.read().splitlines()
        text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = []
        # text_lower_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]
        for w in text_tokens:
            if w.lower() not in lines:
                text_tokens_without_stopwords.append(w)

        # text_tokens_without_stopwords = [w for w in text_tokens if w not in f.read()]
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

        new_tokenized_text = []
        tokenized_text1 = self.parse_sentence(full_text) # TODO what is doc_length and why

        tokenized_text = self.text_to_tokenize(full_text)
        tokenized_retweet = self.text_to_tokenize(retweet_text)
        tokenized_quote = self.text_to_tokenize(quote_text)
        tokenized_url = self.handle_url(url)
        tokenized_retweet_url = self.handle_url(retweet_url)
        tokenized_quote_text = self.handle_url(quote_url)

        doc_length = len(tokenized_text1)  # after text operations - length of full_text

        # our rules: numbers? emojis? spelling mistakes? bed.Today?

        new_tokenized_text = tokenized_text + tokenized_retweet + tokenized_quote + tokenized_url + tokenized_retweet_url + tokenized_quote_text

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

    def text_to_tokenize(self, text):
        old_token = self.parse_sentence(text)
        doc_length = len(old_token)
        num_dict = {"thousand": "K", "million": "M", "billion": "B", "dollar": "$", "dollars": "$", "percent": "%",
                    "percentage": "%"}

        new_tokenized_text = []

        for i in range(doc_length):
            term = old_token[i]
            next_term = None
            if i + 1 < doc_length:
                next_term = old_token[i + 1]
            if term is "@":
                new_tokenized_text.append(self.handle_tags(next_term))
            elif term is "#":
                new_tokenized_text.extend(self.handle_hashtag(next_term))
            elif str.isdigit(term.replace(",", "")):  # if term is a number
                # deal with decimal number like 10.1234567 -> 10.123
                num = str(term.replace(",", ""))
                if float(num) > 999:
                    num = self.numbers_over_1K(term)
                if next_term is not None and next_term.lower() in num_dict.keys():
                    new_tokenized_text.append(num + num_dict[next_term])
                else:
                    new_tokenized_text.append(num)
            else:
                new_tokenized_text.append(self.upper_or_lower(term))
        return new_tokenized_text
