
import os
import heapq
import pickle

from Trie import *
from Preprocessing import *

def parseDirectory(directory, verbose = False):
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
    num_documents, tree = parseDirectory(directory, True)
    writeData((num_documents, tree), '.\\data_index.dat')

def loadIndex():
    return readData('.\\data_index.dat')


#directory = os.path.join('.', 'private')
#createIndex(os.path.join('.', 'data'))
#num_documents, tree = loadIndex()

#with open('./view.txt', 'w', encoding='utf-8') as f:
#    f.write(str(num_documents) + '\n\n')
#    f.write(str(tree))


# precedence: not and or
def searchQuery(query, tree, num_docs):
    query = re.sub(r'\s+', ' ',   query)			# remove duplicated spaces
    query = query.strip()
    
    for or_term in query.split('or'):
        or_term = or_term.strip()
        for and_term in or_term:
            and_term.strip()
            if and_term.startswith('not '):
                and_term = and_term[4:-1]
            
    

'''
while(True):
    query = input('\nQuery: ')
    print('Searching:', query)
    if(query):
        words = extractWords(query, True)
        print(words)
'''