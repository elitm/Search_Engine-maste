from nltk.corpus import stopwords

from reader import ReadFile
from parser_module import Parse
import os


def main():
    # rf = ReadFile("C:\\Users\Chana\Documents\SearchEngine\Data") # corpus
    # rf.read_all_files_from_corpus()

    rf2 = ReadFile("C:\\Users\elitm\PycharmProjects\Search_Engine-maste")
    list2D = rf2.read_file("sample2.parquet")
    #print(list2D)
    # print(os.getcwd())
    parse1 = Parse()
    # hashtag function testing
    # print(parse.handle_hashtag("iLoveFood"))
    # print(parse.handle_hashtag("ILoveFood"))
    # print(parse.handle_hashtag("i_love_food"))
    # for i in range (len(list2D)):
    doc = parse1.parse_doc(list2D[73])
    print(doc.doc_id)

    #parse1.handle_url("https://twitter.com/i/web/status/1280943769077141507")

    # print(doc.quote_text)
    # print("\n")
    # print(doc.full_text)
    # print(parse.numbers_over_1K("55,442"))
    # print(parse.simple_numbers_over_1K("10,123,000"))
    # x = int(float("1010.56"))
    # y = int(float("10,123".replace(",","")))

    # for lst in list2D:
    #     lst = [x if x is not None else '' for x in lst] # replace None with ''
    #     stringy = ''.join(lst)
    #     print(parse.parse_sentence(stringy))
        # print(stringy)
    # print(stopwords.words('english'))


if __name__ == "__main__":
    main()
