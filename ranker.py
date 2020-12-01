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
        vectors_for_doc = [np.zeros(25)]
        doc_value_dict = {} # key: doc(tweet id), value: avg vector - value of doc
        glove_file = open('glove.twitter.27B.25d.txt', encoding="utf8")
        for line in glove_file:
            records = line.split()
            word = records[0]
            vector = np.asarray(records[1:], dtype='float32')
            vector_dict[word] = vector
        glove_file.close()

        for doc in relevant_docs:
            tweet_id = doc[0]
            modulo = int(tweet_id) % 10
            tweet_term_dict = documents_dict[modulo][tweet_id][0]
            for term in tweet_term_dict:
                if term in vector_dict:
                    vectors_for_doc.append(vector_dict[term])
            # if np.add.reduce(vectors_for_doc) is not np.nan or len(vectors_for_doc) != 0:
            doc_value_dict[tweet_id] = np.add.reduce(vectors_for_doc)/len(vectors_for_doc)

            vectors_for_doc = [np.zeros(25)]

        vectors_for_query = []
        for term in query_as_list:
            if term in vector_dict:
                vectors_for_query.append(vector_dict[term])
        query_vector = np.add.reduce(vectors_for_query)/len(vectors_for_query)

        docs_to_return = []
        for tweet_id in doc_value_dict:
            cos_sim = np.dot(doc_value_dict[tweet_id], query_vector) / (norm(doc_value_dict[tweet_id]) * norm(query_vector))
            docs_to_return.append((cos_sim, tweet_id))

        # return sorted(relevant_docs.items(), key=lambda item: item[1], reverse=True)
        docs_to_return = sorted(docs_to_return, key=lambda element: element[0], reverse=True)
        return docs_to_return[:2000]


    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=1):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: array of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        if k > 2000:
            k = 2000
        return sorted_relevant_doc[:k]
