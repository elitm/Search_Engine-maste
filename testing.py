import timeit

from indexer import Indexer
from reader import ReadFile
from parser_module import Parse
import numpy as np
from configuration import ConfigClass
import os
import string
import re
from searcher import Searcher
import utils
from collections import Counter

def main():
    # rf = ReadFile("C:\\Users\Chana\Documents\SearchEngine\Data") # corpus
    # rf.read_all_files_from_corpus()
    # rf2 = ReadFile("C:\\Users\elitm\PycharmProjects\Search_Engine-maste")
    # rf2 = ReadFile("C:\\Users\Chana\Documents\SearchEngine\Search_Engine-master")
    # list2D = rf2.read_file("sample3.parquet")
    # print(list2D)
    # for_check=['1280966288916066308', 'Wed Jul 08 20:45:37 +0000 2020', 'RT @AAnimatorYellow: Nobody:\nBored (chinese))
    for_check = ['chinดุลnบาสเวิร์คช็อป animators during quarantine: https://t.co/uxOsknVIG1', '[]', '[]','Nobody:\nBored animators during quarantine: https://t.co/uxOsknVIG1', '[]','[]',"",'[]','[]',"",'[]','[]']
    # print(os.getcwd())

    parse1 = Parse(False)
    # url = parse1.handle_url("https://www.instagram.com/p/CD7fAPWs3WM/?igshid=09kf0ugp1l8x")
    # print(url)

    # parse1 = Parse(False)
    # entity = "Dounald Trump Is The Loser no lucky for me"
    # parse1.handle_entity(entity)
    # for_check = ['1280966288916066308', 'Wed Jul 08 20:45:37 +0000 2020','Dounald Trump Is The Loser no lucky for me https://t.co/uxOsknVIG1', '[]', '[]',
    #              'Nobody:\nBored animators during quarantine: https://t.co/uxOsknVIG1', '[]', '[]', "", '[]', '[]', "",
    #              '[]', '[]']
    # doc = (parse1.parse_doc(for_check))
    # print(doc.term_doc_dictionary)
    # config = ConfigClass()
    # indexer1 = Indexer(config)
    # full_doc = parse1.parse_sentence(for_check)
    # print(full_doc)
    # indexer1.add_new_doc(full_doc)
    # indexer1.add_to_file()
    # print(FullDoc.term_doc_dictionary)
    # print(indexer1.inverted_idx)
    # print(indexer1.posting_dict)
    # strat=time.time()
    # for i in range(50000000):
    #     x=5
    # end=time.time()
    # timey=(end-strat)/60
    # print(timey)
    # print(parse1.parse_sentence("I have 2³ strowberries"))
    # chinese = "ดุลnบาสเวิร์คช็อป"
    # print(parse1.parse_sentenceese")

    # print({letter: [] for letter in string.ascii_lowercase + "@#1"})

    # print("@Hanna".lower())
    # hashtag function testing
    # print(parse.handle_hashtag("iLoveFood"))
    # print(parse.handle_hashtag("ILoveFood"))
    # print(parse.handle_hashtag("i_love_food"))

    # tuple_list = [(1,2),(3,4),(5,6)]
    # print("stringy" + str(tuple_list))


    # for i in range(len(list2D)):
    #     doc = parse1.parse_doc(list2D[i])
    #     print(doc.doc_id)
    #
    # print(list2D[0])
    # print(parse1.parse_doc(list2D[0]))
    # print(parse1.parse_sentence("100 thousand dollars"))

    # print(type(⅕))
    # print(A.encode('ascii', 'ignore'))

    # print(doc.quote_text)
    # print("\n")
    # print(doc.full_text)
    # print(parse.numbers_over_1K("55,442"))
    # print(parse.simple_numbers_over_1K("10,123,000"))

    # for lst in list2D:
    #     lst = [x if x is not None else '' for x in lst] # replace None with ''
    #     stringy = ''.join(lst)
    #     print(parse.parse_sentence(stringy))
        # print(stringy)
    # print(stopwords.words('english'))
    # glove_file = open('glove.twitter.27B.200d.txt', encoding="utf8")




    # relevant_docs = searcher.relevant_docs_from_posting(query_parsed)
    # print(len(relevant_docs))

    # print(relevant_docs)
    # print(docs['1281010103487836160'])
    # print(searcher.cos_sim(query_parsed, '1281010103487836160'))

    # doc_tup = [(1,2),(2,2),(4,3),2]
    # for elem in doc_tup[:-1]:
    #     print(elem)

    # a = np.array([100, 100, 6])
    # b = np.array([4, 2, 100])
    # my_list = [a, b]
    # add = np.add.reduce(my_list)
    # print(add/len(my_list))


    # start = timeit.default_timer()
    #
    # query = "Dr. Anthony Fauci wrote in a 2005 paper published in Virology Journal that hydroxychloroquine was effective in treating SARS"
    # query_parsed = parse1.parse_sentence(query)
    # inverted = utils.load_obj("inverted_idx")
    # searcher = Searcher(inverted)
    # relevant_docs, documents_dict = searcher.relevant_docs_from_posting(query_parsed)
    # end_rel = timeit.default_timer()
    # print("searcher: " + str(end_rel-start) + " seconds")
    #
    # ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs, documents_dict, query_parsed)
    # end_rank = timeit.default_timer()
    # print("ranker: " + str(end_rank-start) + " seconds")
    #
    # print("relevant:")
    # print(relevant_docs[:5])
    # print("ranked:")
    # print(ranked_docs[:5])



    # check the tweet that came back as relevant after tweet
    d5 = utils.load_obj("document5")
    d8 = utils.load_obj("document8")
    d9 = utils.load_obj("document9")

    print("relevant 1:")
    print(d5['1291114301873414145']) #relevant 1
    print("relevant 2:")
    print(d8['1281073485431922688']) #relevant 2

    print("ranked 1:")
    print(d8['1284284916591730688']) #ranked 1
    print("ranked 2:")
    print(d9['1290899730969563139'])

    # check the tweet that came back as relevant after tweet: "coronavirus eat bat soup"
    # d5 = utils.load_obj("document5")
    # # print("relevant 1:")
    # # print(d5['']) #relevant 1
    # d8 = utils.load_obj("document8")
    # print("ranked 1:")
    # print(d8['1290606964586631168']) #ranked 1
    # print("ranked 2:")
    # print(d5['1284506827535704065'])





if __name__ == "__main__":
    main()
