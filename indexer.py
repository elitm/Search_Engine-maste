import os
import string
import pickle


class Indexer:

    def __init__(self, config):

        self.inverted_idx = {}
        self.posting_dict = {}
        self.config = config
        # # open files for posting
        # for lower_letter in string.ascii_lowercase:
        #     open(lower_letter + ".txt", 'a')
        # # for upper_letter in string.ascii_uppercase:
        # #     open(upper_letter + ".txt", 'a')
        # open("@.txt", 'a') # all other characters
        for lower_letter in string.ascii_lowercase:
            f = open(lower_letter + ".pkl", 'wb')
            f.close() # need this???
        f2 = open("@.pkl", 'wb')
        f2.close()


    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        document_dictionary = document.term_doc_dictionary
        # Go over each term in the doc
        for term in document_dictionary:
            try:
                # Update inverted index and posting
                if term not in self.inverted_idx:
                    self.inverted_idx[term] = 1
                    self.posting_dict[term] = []
                else:
                    self.inverted_idx[term] += 1

                self.posting_dict[term].append((document.tweet_id, document_dictionary[term]))

            except:
                print('problem with the following key {}'.format(term[0]))

    def add_to_file(self):

        # for term in self.posting_dict:
        #     if len(term) > 0: # TODO fix
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
        for term in self.posting_dict:
            if len(term) > 0:
                if not term[0].isalpha():
                    term = "@" + term
                # if os.path.isfile(term[0] + "Temp.pkl"):
                #     pickle.dump([term, self.posting_dict[term]], f)
                # else:
                with open(term[0] + "Temp.pkl", 'wb') as f:
                    if not term[0].isalpha():
                        term = term[1:]
                    pickle.dump([term,self.posting_dict[term]], f)





    def merge_files(self, filename1, filename2):
        # # Use `with` statements to close file automatically
        # with open(filename1, 'a') as file, open(filename2, 'r') as tempfile:
        #     list_of_files = str(file) + str(tempfile)
        #     # list_of_files.sort()
        #     file.write(list_of_files)
        pass