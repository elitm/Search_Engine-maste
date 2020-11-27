# from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
import re

import utils
from document import Document
from stemmer import Stemmer


class Parse:

    def __init__(self, stem):
        # self.stop_words = stopwords.words('english')
        self.stemming = stem
        with open('stop_words.txt', 'r') as f:
            self.our_stop_words = f.read().splitlines()
        self.stop_words_dict = {key: None for key in self.our_stop_words}
        self.uppercase_dict = dict.fromkeys(string.ascii_uppercase)
        for key in self.uppercase_dict:
            self.uppercase_dict[key] = set()

    # self.lowercase_dict = dict.fromkeys(string.ascii_lowercase, "")
    # for i in self.lowercase_dict.keys():
    #     self.lowercase_dict[i] = os.getcwd() + "\\" + i + ".txt"
    #
    # self.uppercase_dict = dict.fromkeys(string.ascii_uppercase, "")
    # for j in self.uppercase_dict.keys():
    #     self.uppercase_dict[j] = os.getcwd() + "\\" + j + ".txt"
    #
    # self.other_chars = os.getcwd() + "\\" + "other_chars.txt"  # will hold file with text beginning in characters that are not letters (numbers, #, $...)

    def handle_hashtag(self, hashtag_str: str):
        glue = ' '
        if hashtag_str.__contains__("_"):
            result = hashtag_str.split("_")
        else:  # separate by uppercase letters
            result = ''.join(glue + x.lower() if x.isupper() else x for x in hashtag_str).strip(glue).split(glue)
        result.append("#" + hashtag_str.lower().replace("_", ""))

        return result

    def handle_numbers(self, num_as_str):
        num = int(float(num_as_str.replace(",", "")))
        if num < 1000:
            return num_as_str
        k = pow(10, 3)
        m = pow(10, 6)
        b = pow(10, 9)
        if k <= num < m:
            return str(int(num / k)) + "K"
        if m <= num < b:
            return str(int(num / m)) + "M"
        if num >= b:
            return str(int(num / b)) + "B"

    def handle_tags(self, tag_string):
        return "@" + tag_string

    def upper_or_lower(self, word_to_check):
         if word_to_check[0].isupper():
            self.uppercase_dict[word_to_check[0]].add(word_to_check)
            return str.upper(word_to_check)
         return word_to_check


    def handle_url(self, url_token: str):
        if url_token is None:
            return []
        url_token = url_token[8:]

        split_url = []
        space_or_char = ""

        for char in url_token:
            if char == "/" and space_or_char != "":
                split_url.append(space_or_char)
                space_or_char = ""
                break
            else:
                space_or_char += char
        return split_url

    # our rule 1: remove emojis from tweets
    def remove_emojis(self, txt):
        re_emoji = re.compile("["
                              u"\U0001F600-\U0001F64F"  # emoticons
                              u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                              u"\U0001F680-\U0001F6FF"  # transport & map symbols
                              "]+", flags=re.UNICODE)
        word = re_emoji.sub(r'', txt)
        return word

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:
        """

        if text is None:
            return []
        text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = []
        # text_lower_tokens_without_stopwords = [w.lower() for w in text_tokens if w not in self.stop_words]

        # remove stopwords
        for w in text_tokens:
            if w.lower() not in self.stop_words_dict:
                text_tokens_without_stopwords.append(w)

        # parsing
        doc_length = len(text_tokens_without_stopwords)
        num_dict = {"thousand": "K", "million": "M", "billion": "B", "dollar": "$", "dollars": "$", "percent": "%",
                    "$": "$", "%": "%",
                    "percentage": "%"}
        # try: #TODO remove
        new_tokenized_text = []
        i = -1
        # for i in range(doc_length):
        while i < doc_length - 1:
            # please note: when we do i += 1 it is because next_term(old_token[i + 1]) is used already so we skip over it next iteration
            # so we dont go over it twice

            i += 1
            term = text_tokens_without_stopwords[i]
            # if term.__contains__("ดุ"):
            #     print("ดุลบาสเวิร์คช็อป")
            term = term.encode("ascii", "ignore").decode()  # remove ascii
            # term = re.sub(r'[^\x00-\x7f]', r'', term)
            next_term = None
            if term.startswith("//t") or (term.isalpha() and len(term) == 1):
                continue
            if term.__contains__("-"):
                new_tokenized_text.extend(term.split("-"))
            if i + 1 < doc_length:
                next_term = text_tokens_without_stopwords[i + 1]
            if term is "@" and next_term is not None:
                new_tokenized_text.append(self.handle_tags(next_term))
                i += 1
            elif term is "#" and next_term is not None:
                new_tokenized_text.extend(self.handle_hashtag(next_term))
                i += 1
            elif term is "$" and next_term is not None and str.isdigit(
                    next_term.replace(",", "")):  # $100 thousand / $75 --> 100K$ / 75$
                num = self.handle_numbers(next_term)
                if i + 2 < doc_length and text_tokens_without_stopwords[i + 2] in num_dict:
                    num = num + num_dict[text_tokens_without_stopwords[i + 2]]
                    i += 1
                new_tokenized_text.append(num + "$")
                i += 1
            elif str.isdigit(term.replace(",", "")):  # if term is a number
                # deal with decimal number like 10.1234567 -> 10.123
                num = self.handle_numbers(term)
                if next_term is not None and next_term.lower() in num_dict:
                    new_tokenized_text.append(num + num_dict[next_term.lower()])
                    i += 1
                else:
                    new_tokenized_text.append(num)
            elif not term.isidentifier():  # identifier: (a-z) and (0-9), or underscores (_)
                emojis_removed = self.remove_emojis(term)
                if emojis_removed is not "":
                    new_tokenized_text.append(emojis_removed)
            else:
                new_tokenized_text.append(self.upper_or_lower(term))
                if next_term is not None and term[0].isupper() and next_term[0].isupper():
                    new_tokenized_text.append(str.upper(term) + " " + str.upper(next_term))  # names

        return new_tokenized_text
        # except:
        #     return new_tokenized_text

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """
        # tweet_id = doc_as_list[0]
        # tweet_date = doc_as_list[1]
        # full_text = doc_as_list[2]
        # url = doc_as_list[3]
        # retweet_text = doc_as_list[4]
        # retweet_url = doc_as_list[5]
        # quote_text = doc_as_list[6]
        # quote_url = doc_as_list[7]

        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        indice = doc_as_list[4]  # TODO why do we fking need indices
        retweet_text = doc_as_list[5]
        retweet_url = doc_as_list[6]
        retweet_indice = doc_as_list[7]
        quote_text = doc_as_list[8]
        quote_url = doc_as_list[9]
        quoted_indice = doc_as_list[10]
        retweet_quoted_text = doc_as_list[11]
        retweet_quoted_url = doc_as_list[12]
        retweet_quoted_indice = doc_as_list[13]

        term_dict = {}

        tokenized_text = self.parse_sentence(full_text)
        # tokenized_retweet = self.parse_sentence(retweet_text)
        tokenized_quote = self.parse_sentence(quote_text)
        tokenized_url = self.handle_url(url)
        # tokenized_retweet_url = self.handle_url(retweet_url)
        # tokenized_quote_url = self.handle_url(quote_url)
        #
        # tokenized_rt_quote_text = self.parse_sentence(retweet_quoted_text)
        # tokenized_rt_quoted_url = self.handle_url(retweet_quoted_url)

        doc_length = len(tokenized_text)  # after text operations - length of full_text

        # our rules: dollars? emojis? bed.Today? sentences-like-this? #ILOsummit

        # new_tokenized_text = tokenized_text + tokenized_retweet + tokenized_quote + tokenized_url + tokenized_retweet_url + tokenized_quote_url +\
        #     tokenized_rt_quote_text + tokenized_rt_quoted_url
        new_tokenized_text = tokenized_text + tokenized_url + tokenized_quote

        if self.stemming is True:
            s = Stemmer()
            for token in new_tokenized_text:
                new_tokenized_text.append(s.stem_term(token))
                new_tokenized_text.remove(token)

        for term in new_tokenized_text:
            # print(term)
            if term is not "":  # or (term.isalpha() and len(term) == 1)
                if term not in term_dict:
                    term_dict[term] = 1
                else:
                    term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)

        return document

    def remove_big_letters_word(self, inverted_idx):
        word_in_lower_and_upper = []

        for letter in self.uppercase_dict:
            upper_to_lower_words = [x.lower() for x in list(self.uppercase_dict[letter])] # check if word whom found in upper case also found in lower
            for word in upper_to_lower_words:
                if word in inverted_idx:
                    word_in_lower_and_upper.append(word)

            letter_posting_file = utils.load_obj(letter)
            for word in word_in_lower_and_upper:
                if word.upper() in letter_posting_file:
                    word_appearance = letter_posting_file[word.upper()]
                    letter_posting_file[word].append(word_appearance)
                    del letter_posting_file[word.upper()]
            utils.save_obj(letter_posting_file, letter)
