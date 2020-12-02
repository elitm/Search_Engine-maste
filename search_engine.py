import os

from reader import ReadFile
from configuration import ConfigClass
from parser_module import Parse
from indexer import Indexer
from searcher import Searcher
import utils


def run_engine(config):
    """
    :return:
    """
    number_of_documents = 0

    if config.toStem:
        if not os.path.exists(config.savedFileMainFolder + "\\WithStem"):
            os.makedirs(config.savedFileMainFolder + "\\WithStem")
        out = config.saveFilesWithStem
    else:
        if not os.path.exists(config.savedFileMainFolder + "\\WithoutStem"):
            os.makedirs(config.savedFileMainFolder + "\\WithoutStem")
        out = config.saveFilesWithoutStem
    out += '\\'

    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse(config.toStem)
    indexer = Indexer(config, out)

    end_of_corpus = False

    for documents_list in r:
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = p.parse_doc(document)
            number_of_documents += 1
            if r.queue.empty() and number_of_documents == len(documents_list) - 1:
                end_of_corpus = True
            # index the document data
            indexer.add_new_doc(parsed_document, end_of_corpus)
            if end_of_corpus:
                end_of_corpus = False

    for letter in indexer.ABC_dict:
        for idx in range(1, (indexer.counter_dict_files[letter]) + 1):
            indexer.merge_files(indexer.out, letter, letter + str(idx))
            os.remove(out + letter + str(idx) + ".pkl")

    p.remove_uppercase_and_entities(indexer)
    indexer.sort_tweet_ids()
    utils.save_obj(indexer.inverted_idx, "inverted_idx")



def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def search_and_rank_query(query, inverted_index, k, config):
    p = Parse(config.toStem)
    query_as_list = p.parse_sentence(query)
    searcher = Searcher(inverted_index, config)
    relevant_docs, documents_dict = searcher.relevant_docs_from_posting(query_as_list)
    ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs, documents_dict, query_as_list)
    return searcher.ranker.retrieve_top_k(ranked_docs, k)


def main(corpus_path, output_path, stemming, queries, num_doc_to_retrieve):
    config = ConfigClass()
    config.corpusPath = corpus_path
    config.savedFileMainFolder = output_path
    config.toStem = stemming

    run_engine(config)
    inverted_index = load_index()
    queries_file = open(queries, encoding="utf8")
    tuple_answers = []
    query_num = 1
    for query in queries_file:
        for doc_tuple in search_and_rank_query(query[:-1], inverted_index, num_doc_to_retrieve, config):
            print('tweet id: {} Score: {}'.format(doc_tuple[0], doc_tuple[1]))
            doc_tuple = doc_tuple + (query_num,)
            tuple_answers.append(doc_tuple)
        query_num += 1
    queries_file.close()




