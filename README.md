<h3>Information Retrieval Search Engine</h3>
---------------------------

search engine written in **Python** using NLP and informational retrieval algorithms with a data set of over 10,000,000 tweets.

The project was built in two programming phases – indexing and retrieving.

<h4>Indexing the Documents</h4>

The corpus includes approximately 10,000,000 tweets. The corpus is a very large database that cannot exist on RAM alone. Therefore, we work on the information in small iterations of 500,000 tweets in each iteration. In addition, this reduces running time.
Each Tweet will be divided into Tokens according to the rules defined in the parser. The parser will return a document that contains the words with more information about the Tweet, information that will also be used by us in Indexer.


Some of the project’s main classes for this part:

ReadFile – Receives a path to the folder of the corpus, reads the files in it and separates the documents.

Parser – Separates every tweet to tokens according to specific parsing rules regarding general words, numbers, dates and timestamps and etc.

Stemmer – Stemming is the process of reducing inflected (or sometimes derived) words to their word stem, base or root form. implemented using an open-source stemmer.


<h4>Retrieving Relevant Documents </h4>

Our engine receives either a single query or a path to a file containing multiple queries. The parser class on the query (or queries) is used to match the query to the dictionary.
Documents that match the query are retrieved by the engine.

<h5>Project’s main classes for Retrieving part:</h5>

Searcher – The term from the query is searched in all letter posting files matching the query and the document list for each term is obtained. The united list of documents for the query is then passed to the Ranker class for sorting by relevance.

Ranker – Rates the relevance of each document to the query. Returns K most relevent documents by score. score is calculate at score class. 

Score - Stores the necessary data of every document to calculate its score. Score use **'GolVe'** modle to find score similarity. we calculate the angle between the tweet (dcument) vector to the query vector.

NLP modles uses at score class - **Word2Vec**,**Word2Vec**, **WordNet**, **Thesaurus**
