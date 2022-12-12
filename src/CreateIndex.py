
import os
import heapq
import pickle

from Trie import *
from Preprocessing import *

def createIndex(directory, verbose = False):
    tree = Trie()
    num_documents = 0

    for (dirpath, _, filenames) in os.walk(directory):
        for file in filenames:
            name = os.path.join(dirpath, file)
            if file.endswith('.pdf'):
                verbose and print('Processing file:', name)
                num_documents += 1
                text_content = loadText(name)
                words, max_freq, _ = extractWords(text_content)
                for (word, num) in words:
                    heap = tree.get(word)
                    if heap is None:
                        heap = []
                        tree.put(word, heap)
                    heapq.heappush(heap, (-num/max_freq, name)) # negative (heapq has a minimum priority)
    return num_documents, tree

def readData(fileName):
    with open(fileName, 'rb') as f:
        bindata = f.read()
        data = pickle.loads(bindata)
        return data

def writeData(data, fileName):
    with open(fileName, 'wb') as f:
        bindata = pickle.dumps(data)
        f.write(bindata)


def createIndex(directory):
    print(directory)
    num_documents, tree = createIndex(directory, True)
    writeData((num_documents, tree), '.\\data_index.dat')

def loadIndex():
    return readData('.\\data_index.dat')


#directory = os.path.join('.', 'private')
#num_documents, tree = loadIndex()
'''
    with open('./view.txt', 'w', encoding='utf-8') as f:
    f.write(str(num_documents) + '\n\n')
    f.write(str(tree))
'''

# precedence: not and or
def searchQuery(query):
    query = re.sub(r'\s+', ' ',   query)			# remove duplicated spaces
    query = query.strip()
    
    and_sent = query.split('or')

while(True):
    query = input('\nQuery: ')
    print('Searching:', query)
    if(query):
        words = extractWords(query, True)
        print(words)