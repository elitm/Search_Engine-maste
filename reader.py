import os
import pandas as pd


class ReadFile:
    def __init__(self, corpus_path):
        self.corpus_path = corpus_path

    def read_file(self, file_name):
        """
        This function is reading a parquet file contains several tweets
        The file location is given as a string as an input to this function.
        :param file_name: string - indicates the path to the file we wish to read.
        :return: a dataframe contains tweets.
        """
        full_path = os.path.join(self.corpus_path, file_name)
        df = pd.read_parquet(full_path, engine="pyarrow")
        # print(df.values.tolist())
        return df.values.tolist()

    def read_all_files_from_corpus(self):
        dirs_in_corpus = os.listdir(self.corpus_path)
        for dirname in dirs_in_corpus:
            joined_name = os.path.join(self.corpus_path, dirname)
            filename = os.listdir(joined_name)
            # print(os.path.join(joined_name, filename[0]))
            print("------------")
            self.read_file(os.path.join(joined_name, filename[0]))



