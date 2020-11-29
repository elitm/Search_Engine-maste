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
        return relevant_docs


    def cos_sim(self, query, relevant_doc):

        count = 0
        max_tf = self.documents[relevant_doc].max_tf
        len_docs = len(self.documents)
        for word in query:
            if word in self.documents[relevant_doc].term_doc_dictionary:
                count += self.documents[relevant_doc].term_doc_dictionary[word]
            w = count / max_tf



