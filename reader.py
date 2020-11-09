import os
import pandas as pd
import glob


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
        # dirs_in_corpus = os.listdir(self.corpus_path)
        # for dirname in dirs_in_corpus:
        #     if dirname.endswith("2020"):
        #         joined_name = os.path.join(self.corpus_path, dirname)
        #         filelist = os.listdir(joined_name)
        #         for filename in filelist:
        #             if filename.endswith(".snappy"):
        #                 # print(os.path.join(joined_name, file))
        #                 self.read_file(os.path.join(joined_name, filename))
        files = glob.glob(self.corpus_path+'/**/*.parquet')
        for file in files:
            self.read_file(file)