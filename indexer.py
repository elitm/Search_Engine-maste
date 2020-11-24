import re
import string
import pickle
import utils


class Indexer:

    def __init__(self, config):

        self.inverted_idx = {}
        self.posting_dict = {}
        self.config = config

        for lower_letter in string.ascii_lowercase + "@":
            f = open(lower_letter + ".pkl", 'wb')
            pickle.dump([], f)
            f.close() # need this???



    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        max_tf = 0
        unique_terms_counter = 0
        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary:
            try:
                if term == "ดุลnบาสเวิร์คช็อป":
                    print("found chinese")
                # Update inverted index and posting
                if term not in self.inverted_idx:
                    self.inverted_idx[term] = 1
                    self.posting_dict[term] = []
                    unique_terms_counter += 1
                else:
                    self.inverted_idx[term] += 1

                max_tf = max(self.inverted_idx[term], max_tf)

                self.posting_dict[term].append((document.tweet_id, document_dictionary[term])) # key: str , value: array of tuples

            except:

                print('problem with the following key {}'.format(term[0]))
        document.max_tf = max_tf
        document.unique_terms = unique_terms_counter

    def add_to_file(self):

        # for term in self.posting_dict:
        #     if len(term) > 0:
        #         print(term)
        #         if not term[0].isalpha():
        #             term = "@" + term
        #         with open(term[0].lower() + "Temp.txt", 'a') as f: # temp file for merge
        #             if not term[0].isalpha():
        #                 term = term[1:]
        #             f.write(term + ":" + str(self.posting_dict[term]) + "\n")
        # for letter in (string.ascii_lowercase + "@"):
        #     if os.path.isfile(letter + "Temp.txt"): # if file exists
        #         self.merge_files(letter + ".txt", letter + "Temp.txt")
        obj_dict = {letter: [] for letter in string.ascii_lowercase + "@"}
        for term in self.posting_dict:
            # if len(term) > 0: # why would term be empty
            # if not term[0].isalpha():
            if not re.match("^[a-zA-Z]", term):
                obj_dict["@"].append([term, self.posting_dict[term]])
            else:
                obj_dict[term[0].lower()].append([term,self.posting_dict[term]])

        for letter in obj_dict:
            utils.save_obj(obj_dict[letter], letter + "Temp")
            self.merge_files(letter, letter + "Temp")



    def merge_files(self, permanent_file_name, temp_file_name):

        temp_file = utils.load_obj(temp_file_name)
        permanent_file = utils.load_obj(permanent_file_name)
        exists = False
        for temp_term_arr in temp_file:
            for perm_term_arr in permanent_file:
                if perm_term_arr[0] == temp_term_arr[0]: # term exists already so we just add all of the (tweet id, count)
                    exists = True
                    perm_term_arr[1] = self.merge(perm_term_arr[1], temp_term_arr[1])
                    break
            if not exists: # word doesnt exist so we add term and data
                i = self.find_idx(permanent_file, temp_term_arr[0])
                permanent_file.insert(i, temp_term_arr)

        for perm_term_arr in permanent_file: # adds df - data frequency (number of tweets the term is in) to array[2]
            if len(perm_term_arr) == 2:
                perm_term_arr.append(len(perm_term_arr[1]))

        utils.save_obj(permanent_file, permanent_file_name)


    def find_idx(self, arr, val):
        # Searching for the position
        i = 0
        for i in range(len(arr)):
            if arr[i][0].lower() > val.lower():
                return i
        return i+1



    def merge(self, arr1, arr2):
        n1 = len(arr1)
        n2 = len(arr2)
        arr3 = [None] * (n1 + n2)
        i,j,k = 0
        # Traverse both array
        while i < n1 and j < n2:

            if arr1[i] < arr2[j]:
                arr3[k] = arr1[i]
                k = k + 1
                i = i + 1
            else:
                arr3[k] = arr2[j]
                k = k + 1
                j = j + 1

        # Store remaining elements
        # of first array
        while i < n1:
            arr3[k] = arr1[i];
            k = k + 1
            i = i + 1

        # Store remaining elements
        # of second array
        while j < n2:
            arr3[k] = arr2[j];
            k = k + 1
            j = j + 1

        return arr3



