import math

from parser_module import Parse
from ranker import Ranker
import utils


class Searcher:

    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.ranker = Ranker()
        self.inverted_index = inverted_index
        self.documents = utils.load_obj("documents")
        self.letters_files = {}
        self.SIZE = 4000


    def relevant_docs_from_posting(self, query: list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query as list tokenized from our parser
        :return: dictionary of relevant documents.
        """
        letters_in_query_set = set()
        # query = [word.lower() for word in query]
        # query.sort()
        for term in query:
            letters_in_query_set.add(term[0].lower())
        # TODO add check if in inverted index - if not, we dont need to check posting bichlal
        for letter in letters_in_query_set:
            self.letters_files[letter] = utils.load_obj("C:\\Users\Chana\Documents\SearchEngine\Search_Engine-master\output_files\WithoutStem\\" + letter) # TODO fix - get self.out....

        relevant_docs = {}
        for term in query:
            try:
                posting_dict = self.letters_files[term[0]]
                if term in posting_dict:
                    posting_doc = posting_dict[term]
                    for doc_tuple in posting_doc:
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

        count = 0
        mone = 0
        mechane = 0
        max_tf = self.documents[relevant_doc].max_tf
        len_docs = len(self.documents)
        for word in query:
            if word in self.documents[relevant_doc].term_doc_dictionary:
                count += self.documents[relevant_doc].term_doc_dictionary[word]
            w1 = count / max_tf
            posting_dict = self.letters_files[word[0]]
            count_doc_for_word = posting_dict[word][-1]

            w2 = math.log((len_docs/count_doc_for_word), 2)
            mone += w1 * w2
            mechane += math.pow(w1*w2, 2)


        mechane = math.sqrt(mechane) # TODO

        return mone/mechane




