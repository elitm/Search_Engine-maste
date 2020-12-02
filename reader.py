import os
import queue
import pandas as pd
import glob


class ReadFile:

    def init_queue(self):
        for (root, dirs, files) in os.walk(self.corpus_path, topdown=True):
            for file in files:
                try:
                    if file[-8:] == ".parquet":
                        self.queue.put(root + '/' + file)
                except:
                    continue

    def __init__(self, corpus_path):
        self.corpus_path = corpus_path
        self.queue = queue.Queue()
        self.init_queue()

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
        files = glob.glob(self.corpus_path+'/**/*.parquet')
        for file in files:
            self.read_file(file)

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue.empty():
            raise StopIteration
        file_path = self.queue.get()
        return self.read_file(file_path)