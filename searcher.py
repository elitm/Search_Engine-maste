import math
from ranker import Ranker
import utils
from collections import Counter

class Searcher:

    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.documents = utils.load_obj("documents")
        self.letters_files = {}
        self.query_terms_count = {}
        self.max_term_in_query = 0
        self.SIZE = 4000


    def relevant_docs_from_posting(self, query: list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query as list tokenized from our parser
        :return: dictionary of relevant documents.
        """
        letters_in_query_set = set()

        for term in query:
            letters_in_query_set.add(term[0].lower())
            if term not in self.query_terms_count:
                self.query_terms_count[term] = 1
            else:
                self.query_terms_count[term] += 1

        self.max_term_in_query = max(len(self.query_terms_count), max(self.query_terms_count.values()))

        # TODO add check if in inverted index - if not, we dont need to check posting bichlal
        for letter in letters_in_query_set:
            self.letters_files[letter] = utils.load_obj("C:\\Users\Chana\Documents\SearchEngine\Search_Engine-master\output_files\WithoutStem\\" + letter) # TODO fix - get self.out....

        relevant_docs = {}
        for term in query:
            try:
                posting_dict = self.letters_files[term[0].lower()]
                if term in posting_dict:
                    posting_doc = posting_dict[term]
                    for doc_tuple in posting_doc[:-1]:
                        doc = doc_tuple[0]
                        if doc not in relevant_docs:
                            relevant_docs[doc] = 1
                        else:
                            relevant_docs[doc] += 1
            except:
                print('term {} not found in posting'.format(term))

        doc_weights = {}
        for doc in relevant_docs:
            doc_weights[doc] = self.cos_sim(query, doc)

        relevant_docs = sorted(doc_weights.items(), key=lambda x: x[1], reverse=True)
        length = min(len(relevant_docs), self.SIZE)
        return relevant_docs[:length]


    def cos_sim(self, query, relevant_doc):

        count_word_in_doc = 0
        mone = 0
        wij_pow = 0
        wiq_pow = 0

        max_tf = self.documents[relevant_doc].max_tf
        len_docs = len(self.documents)
        for word in query:
            if word in self.documents[relevant_doc].term_doc_dictionary:
                count_word_in_doc += self.documents[relevant_doc].term_doc_dictionary[word]
            else:
                continue
            w1 = count_word_in_doc / max_tf
            posting_dict = self.letters_files[word[0].lower()]
            count_doc_for_word = posting_dict[word.lower()][-1]

            w2 = math.log((len_docs/count_doc_for_word), 2)
            w3 = self.query_terms_count[word]/self.max_term_in_query # *1 query


            mone += w1 * w2 * w3
            wij_pow += math.pow(w1*w2, 2)
            wiq_pow += math.pow(w3, 2)

        mechane = math.sqrt(wij_pow*wiq_pow)
        # if mechane == 0:
        #     print(w1)
        #     print(w2)
        #     print(w3)


        return mone/mechane




