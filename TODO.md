
# PDF Information Retrieval System

- [x] Extract text from PDF files
- [x] Perform NLP pre-processing by TF-IDF representation
- [x] Perform Parts of speech tagging selecting only the nouns
- [x] Create inverted index through of a radix tree
- [x] Store the inverted index
- [ ] Create the query system using boolean expressions (and, or and not operators)
- [ ] Develop a web system to performs queries

# Report

We are using R with pdftools to extract text over Pyhon with PyPDF. The last can not handle correctly the spaces among words.

The words uses the frequency representation and tf-idf in the queries.

We keep the single nouns and sequences of two or three nouns. The terms two or three nouns, a adjective or adverb can replace the first or the last noun.

The inverted index uses a Trie representation with charactere keys allowing prefixes. The values are heap priority queues with the frequency of the key and the corresponding path to the document.

We stores the inverted index writing the Trie and number of documenta in the file data_index.dat using binary mode.

# Future Works

- [ ] 

# References

[http://thomas-cokelaer.info/blog/2013/01/r-warnings-when-starting-tpy2/]
[https://stackoverflow.com/questions/50585315/calling-a-r-function-from-python-code-with-passing-arguments]
[https://medium.com/product-ai/text-preprocessing-in-python-steps-tools-and-examples-bf025f872908]
[https://www.guru99.com/pos-tagging-chunking-nltk.html]
[https://sigmoidal.ai/como-criar-uma-wordcloud-em-python/]