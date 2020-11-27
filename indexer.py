import re
import string
import pickle
import timeit

import utils


class Indexer:

    def __init__(self, config):

        self.DOCS_SIZE = 300000
        self.docs_count = 0

        self.inverted_idx = {}
        self.posting_dict = {}
        self.config = config

        self.a_dict = {} # key: term, val: array of tuples
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

        for lower_letter in string.ascii_lowercase + "@#1":
            f = open(lower_letter + ".pkl", 'wb')
            pickle.dump({}, f)
            f.close() # need this???



    def add_new_doc(self, document, end_of_parquet):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param end_of_parquet: bool if we reached end of parquet
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
                    # self.posting_dict[term] = []
                    unique_terms_counter += 1
                else:
                    self.inverted_idx[term] += 1
                if term not in self.posting_dict:
                    self.posting_dict[term] = []

                self.posting_dict[term].append((document.tweet_id, document_dictionary[term])) # key: str , value: array of tuples

                max_tf = max(self.inverted_idx[term], max_tf)

            except:

                print('problem with the following key {}'.format(term[0]))

        document.max_tf = max_tf
        document.unique_terms = unique_terms_counter
        self.docs_count += 1
        if self.docs_count == self.DOCS_SIZE or end_of_parquet: # if we reach chunk size or end of parquet (so we add the remains)
            self.add_to_file()
            self.docs_count = 0
            self.posting_dict = {}


    def add_to_file(self):

        # for term in self.posting_dict:
        #     # if len(term) > 0: # why would term be empty
        #     # if not term[0].isalpha():
        #     if not re.match("^[a-zA-Z]", term):
        #         obj_dict["@"].append([term, self.posting_dict[term]])
        #     else:
        #         obj_dict[term[0].lower()].append([term,self.posting_dict[term]])

        for term in self.posting_dict:

            if re.match("^[a-zA-Z]", term) or term[0] == "@" or term[0] == "#":
                self.ABC_dict[term[0].lower()][term] = self.posting_dict[term]

            elif term[0].isdigit(): # numbers
                self.ABC_dict["1"][term] = self.posting_dict[term]
            else: # garbage
                continue

        for letter in self.ABC_dict:
            # utils.save_obj(self.ABC_dict[letter], letter + "Temp")
            self.merge_files(letter, self.ABC_dict[letter])
            self.ABC_dict[letter] = {} # empty the dict for next chunk


    def merge_files(self, permanent_file_name, temp_letter_dict):

        start = timeit.default_timer()

        # temp_file = utils.load_obj(temp_file_name)
        permanent_dict_file = utils.load_obj(permanent_file_name)

        for key in temp_letter_dict:
            if key in permanent_dict_file:
                permanent_dict_file[key].extend(temp_letter_dict[key])
            else:
                permanent_dict_file[key] = temp_letter_dict[key]



        utils.save_obj(permanent_dict_file, permanent_file_name)

        end = timeit.default_timer()
        print("merge done")
        print(end - start)


    def sort_tweet_ids(self):
        s = timeit.default_timer()

        for letter in self.ABC_dict:
            letter_dict = utils.load_obj(letter)
            for key in letter_dict:
                letter_dict[key].sort(key=lambda tup: tup[0]) # TODO python sort vs. our own sort: check runtime
            utils.save_obj(letter_dict, letter)

        e = timeit.default_timer()
        print("sorting tweet ids:" + str(e-s) + " seconds")


    # def find_idx(self, arr, val):
    #     # Searching for the position
    #     i = 0
    #     for i in range(len(arr)):
    #         if arr[i][0].lower() > val.lower():
    #             return i
    #     return i+


    # def merge(self, arr1, arr2):
    #     n1 = len(arr1)
    #     n2 = len(arr2)
    #     arr3 = [None] * (n1 + n2)
    #     i = 0
    #     j = 0
    #     k = 0
    #     # Traverse both array
    #     while i < n1 and j < n2:
    #
    #         if arr1[i] < arr2[j]:
    #             arr3[k] = arr1[i]
    #             k = k + 1
    #             i = i + 1
    #         else:
    #             arr3[k] = arr2[j]
    #             k = k + 1
    #             j = j + 1
    #
    #     # Store remaining elements
    #     # of first array
    #     while i < n1:
    #         arr3[k] = arr1[i];
    #         k = k + 1
    #         i = i + 1
    #
    #     # Store remaining elements
    #     # of second array
    #     while j < n2:
    #         arr3[k] = arr2[j];
    #         k = k + 1
    #         j = j + 1
    #
    #     return arr3



