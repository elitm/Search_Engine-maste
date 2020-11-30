import heapq
import numpy as np
from numpy.linalg import norm


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_doc(relevant_docs: list, documents_dict:dict, query_as_list):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param query_as_list:
        :param relevant_docs:
        :param documents_dict:
        :return: sorted list of documents by score
        """
        vector_dict = {}
        vectors_for_doc = []
        doc_value_dict = {} # key: doc(tweet id), value: avg vector - value of doc
        glove_file = open('C:\\Users\Chana\Documents\SearchEngine\glove.twitter.27B.200d.txt', encoding="utf8")
        for line in glove_file:
            records = line.split()
            word = records[0]
            vector = np.asarray(records[1:], dtype='float32')
            vector_dict[word] = vector
        glove_file.close()

        for tweet_id in relevant_docs:
            modulo = int(tweet_id) % 10
            tweet_term_dict = documents_dict[modulo][tweet_id][0]
            for term in tweet_term_dict:
                if term in vector_dict:
                    vectors_for_doc.append(vector_dict[term])
        doc_value_dict[tweet_id] = np.add.reduce(vectors_for_doc)/len(vectors_for_doc)

        vectors_for_query = []
        for term in query_as_list:
            if term in vector_dict:
                vectors_for_query.append(vector_dict[term])
        query_vector = np.add.reduce(vectors_for_query)/len(vectors_for_query)

        heap_cosSim = []
        heapq.heapify(heap_cosSim)

        for tweet_id in doc_value_dict:
            cos_sim = np.dot(doc_value_dict[tweet_id], query_vector) / (norm(doc_value_dict[tweet_id]) * norm(query_vector))

            heapq.heappush(heap_cosSim, (-1*cos_sim, tweet_id)) # -1*cos_sim because heap is minimum heap

        return heap_cosSim
        # return sorted(relevant_docs.items(), key=lambda item: item[1], reverse=True)

    @staticmethod
    def retrieve_top_k(sorted_relevant_docs_heap, k=2000):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_docs_heap: heap of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        sorted_relevant_doc = []
        for i in range(k):
            sorted_relevant_doc.append(sorted_relevant_docs_heap.pop)

        # return sorted_relevant_doc[:k]
        return sorted_relevant_doc
