
from indexer import Indexer
from reader import ReadFile
from parser_module import Parse
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


    query = "i like big butts and i cannot lie "
    query_parsed = parse1.parse_sentence(query)
    inverted = utils.load_obj("inverted_idx")
    searcher = Searcher(inverted)
    relevant_docs = searcher.relevant_docs_from_posting(query_parsed)
    docs = utils.load_obj("documents")
    # print(relevant_docs)
    print(docs['1281010103487836160'])
    print(searcher.cos_sim(query_parsed, '1281010103487836160'))

    # doc_tup = [(1,2),(2,2),(4,3),2]
    # for elem in doc_tup[:-1]:
    #     print(elem)



if __name__ == "__main__":
    main()
