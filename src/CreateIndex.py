
import os
import math
import heapq

from Trie import *
from Preprocessing import *

def createIndex(directory):
    tree = Trie()
    num_documents = 0
    document_frequency = {}

    for (dirpath, _, filenames) in os.walk(directory):
        for file in filenames:
            name = os.path.join(dirpath, file)
            if file.endswith('.pdf'):
                num_documents += 1
                words, max_freq, _ = extractWords(name)
                for (word, num) in words:
                    count = 0 if word not in document_frequency else document_frequency[word]
                    document_frequency[word] = count + 1
                    heap = tree.get(word)
                    if heap is None:
                        heap = []
                        tree.put(word, heap)
                    heapq.heappush(heap, (num/max_freq, word, name))
    return tree, document_frequency, num_documents

                
                
directory = os.path.join('.', 'data')
tree,_,_ = createIndex(directory) 
print(tree)
