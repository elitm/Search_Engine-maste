import string
import pickle
import threading
import utils


class Indexer:

    def __init__(self, config, out):
        self.DOCS_SIZE = 500000
        self.docs_count = 0
        self.docs_dict = {}
        self.inverted_idx = {}
        self.posting_dict = {}
        self.config = config
        self.out = out

        self.doc0 = {}
        self.doc1 = {}
        self.doc2 = {}
        self.doc3 = {}
        self.doc4 = {}
        self.doc5 = {}
        self.doc6 = {}
        self.doc7 = {}
        self.doc8 = {}
        self.doc9 = {}
        self.documents = {0: self.doc0, 1: self.doc1, 2: self.doc2, 3: self.doc3,
                          4: self.doc4, 5: self.doc5, 6: self.doc6, 7: self.doc7,
                          8: self.doc8, 9: self.doc9}

        self.counter_dict_files = {k: 0 for k in (string.ascii_lowercase + "@" + "1" + "#")}

        self.a_dict = {}  # key: term, val: array of tuples
        self.b_dict = {}
        self.c_dict = {}
        self.d_dict = {}
        self.e_dict = {}
        self.f_dict = {}
        self.g_dict = {}
        self.h_dict = {}
        self.i_dict = {}
        self.j_dict = {}
        self.k_dict = {}
        self.l_dict = {}
        self.m_dict = {}
        self.n_dict = {}
        self.o_dict = {}
        self.p_dict = {}
        self.q_dict = {}
        self.r_dict = {}
        self.s_dict = {}
        self.t_dict = {}
        self.u_dict = {}
        self.v_dict = {}
        self.w_dict = {}
        self.x_dict = {}
        self.y_dict = {}
        self.z_dict = {}
        self.hashtag_dict = {}
        self.tag_dict = {}
        self.numbers_dict = {}

        self.ABC_dict = {'a': self.a_dict, 'b': self.b_dict,
                         'c': self.c_dict, 'd': self.d_dict,
                         'e': self.e_dict, 'f': self.f_dict,
                         'g': self.g_dict, 'h': self.h_dict,
                         'i': self.i_dict, 'j': self.j_dict,
                         'k': self.k_dict, 'l': self.l_dict,
                         'm': self.m_dict, 'n': self.n_dict,
                         'o': self.o_dict, 'p': self.p_dict,
                         'q': self.q_dict, 'r': self.r_dict,
                         's': self.s_dict, 't': self.t_dict,
                         'u': self.u_dict, 'v': self.v_dict,
                         'w': self.w_dict, 'x': self.x_dict,
                         'y': self.y_dict, 'z': self.z_dict,
                         '1': self.numbers_dict, '#': self.hashtag_dict, '@': self.tag_dict}
        self.letter_counter = {}
        for key in self.ABC_dict:
            self.letter_counter[key] = 0

        for lower_letter in string.ascii_lowercase + "@#1":
            f = open(self.out + lower_letter + ".pkl", 'wb')
            pickle.dump({}, f)
            f.close()  # need this???
        self.docs_files = {}

        for i in range(10):
            with open(self.out + "document" + str(i) + ".pkl", 'wb') as f:
                pickle.dump({}, f)

    def add_new_doc(self, document, end_of_corpus):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param end_of_corpus: bool if we reached end of corpus
        :param document: a document need to be indexed.
        :return: -
        """
        max_tf = 0
        unique_terms_counter = 0
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary:
            try:
                # Update inverted index and posting
                if term not in self.inverted_idx:
                    self.inverted_idx[term] = 1
                    unique_terms_counter += 1
                else:
                    self.inverted_idx[term] += 1
                if term not in self.posting_dict:
                    self.posting_dict[term] = []

                self.posting_dict[term].append(
                    (document.tweet_id, document_dictionary[term]))  # key: str , value: array of tuples

                max_tf = max(document_dictionary[term], max_tf)

            except:

                print('problem with the following key {}'.format(term[0]))

        document.max_tf = max_tf
        document.unique_terms = unique_terms_counter
        self.docs_count += 1

        modulo = int(document.tweet_id) % 10
        self.documents[modulo][document.tweet_id] = [document.term_doc_dictionary, document.max_tf]

        if self.docs_count == self.DOCS_SIZE or end_of_corpus:  # if we reach chunk size or end of corpus
            self.add_to_file(end_of_corpus)
            self.docs_count = 0
            self.posting_dict = {}

            for i in self.documents:  # 0 - 9
                if self.documents[i].__len__() > 15000:
                    doc = utils.load_obj(self.out + "document" + str(i))
                    doc.update(self.documents[i])
                    utils.save_obj(doc, self.out + "document" + str(i))
                    self.documents[i] = {}

    def add_to_file(self, end_of_corpus):

        for term in self.posting_dict:

            if "a" <= term[0] <= "z" or "A" <= term[0] <= "Z" or term[0] == "@" or term[0] == "#":  # TODO remove re
                self.ABC_dict[term[0].lower()][term] = self.posting_dict[term]
                self.letter_counter[term[0].lower()] += 1

            elif term[0].isdigit():  # numbers
                self.ABC_dict["1"][term] = self.posting_dict[term]
                self.letter_counter['1'] += 1
            else:  # garbage
                continue

        thread_list = []

        for letter in self.ABC_dict:
            if self.letter_counter[letter] > 10000 or end_of_corpus:
                self.counter_dict_files[letter] += 1
                chank_num = self.counter_dict_files[letter]
                thread_list.append(threading.Thread(target=utils.save_obj(self.ABC_dict[letter],
                                                                          self.out + letter + str(
                                                                              chank_num))))  # ,args=[self.out + letter + self.chank_num, self.ABC_dict[letter]]))
                self.ABC_dict[letter] = {}  # empty the dict for next chunk
                self.letter_counter[letter] = 0

        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            thread.join()

    def merge_files(self, out, letter, file_name_letter_idx):  # temp_letter_dict):

        permanent_file_name = out + letter
        file_name_letter_idx = utils.load_obj(out + file_name_letter_idx)
        permanent_dict_file = utils.load_obj(permanent_file_name)

        for key in file_name_letter_idx:
            if key in permanent_dict_file:
                permanent_dict_file[key].extend(file_name_letter_idx[key])
            else:
                permanent_dict_file[key] = file_name_letter_idx[key]

        utils.save_obj(permanent_dict_file, permanent_file_name)

    def sort_tweet_ids(self):

        for letter in self.ABC_dict:
            letter_dict = utils.load_obj(self.out + letter)
            for key in letter_dict:
                letter_dict[key].sort(
                    key=lambda tup: tup[0])  # adding length of tupple - number of document the term appears
                letter_dict[key].append(len(letter_dict[key]))
            utils.save_obj(letter_dict, self.out + letter)
