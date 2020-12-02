import os
import queue
import pandas as pd


class ReadFile:

    def init_queue(self):
        for (root, dirs, files) in os.walk(self.corpus_path, topdown=True):
            for file in files:
                try:
                    if file[-8:] == ".parquet":
                        to_put = os.path.join(os.path.relpath(root, self.corpus_path), file)
                        self.queue.put(to_put)
                except:
                    continue

    def __init__(self, corpusPath):
        self.corpus_path = corpusPath
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

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue.empty():
            raise StopIteration
        file_path = self.queue.get()
        return self.read_file(file_path)
