from nltk.corpus import stopwords

from reader import ReadFile
from parser_module import Parse

# import nltk
# nltk.download('stopwords')


def main():
    rf = ReadFile("C:\\Users\Chana\Documents\SearchEngine\Data") # corpus
    rf.read_all_files_from_corpus()

    # rf2 = ReadFile("C:\\Users\Chana\Documents\SearchEngine\Search_Engine-master")
    # list2D = rf2.read_file("sample.parquet")
    # print(list2D)

    # parse = Parse()
    # for lst in list2D:
    #     lst = [x if x is not None else '' for x in lst] # replace None with ''
    #     stringy = ''.join(lst)
    #     print(parse.parse_sentence(stringy))
        # print(stringy)
    # print(stopwords.words('english'))


if __name__ == "__main__":
    main()
