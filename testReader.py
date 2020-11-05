from nltk.corpus import stopwords

from reader import ReadFile
from parser_module import Parse

# TODO is this download ok?? is it good??
import nltk
# nltk.download('stopwords')


def main():
    # rf = ReadFile("C:\\Users\Chana\Documents\SearchEngine\Data") # corpus
    # rf.read_all_files_from_corpus()

    # rf2 = ReadFile("C:\\Users\Chana\Documents\SearchEngine\Search_Engine-master")
    # txt = rf2.read_file("sample.parquet")
    # parse = Parse()
    # parse.parse_sentence(txt)
    # print(txt)
    print(stopwords.words('english'))


if __name__ == "__main__":
    main()
