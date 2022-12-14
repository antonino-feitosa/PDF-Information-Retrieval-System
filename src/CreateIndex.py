
import os
import sys
import heapq
import pickle
import logging

from Trie import *
from Preprocessing import *

def parseDirectory(directory, fileName = '.\\data_index.dat', clear = False, verbose = False):
    processed = []
    tree = Trie()
    if not clear:
        try: processed, tree = readData(fileName)
        except: pass

    index = len(processed)
    for (dirpath, _, filenames) in os.walk(directory):
        for file in filenames:
            name = os.path.join(dirpath, file)
            name = os.path.abspath(name)
            if file.endswith('.pdf') and not file in processed:
                verbose and logging.info('Processing file: %s', name)
                try:
                    text_content = loadText(name)
                    words, max_freq = extractWords(text_content)
                    index += 1
                    processed.append(file)
                    for (word, num) in words:
                        heap = tree.get(word)
                        if heap is None:
                            heap = []
                            tree.put(word, heap)
                        heapq.heappush(heap, (-num/max_freq, index)) # negative (heapq has a minimum priority)
                    writeData((processed, tree), fileName)
                    verbose and logging.info('Stored file: %s', name)
                    with open('./view.txt', 'w', encoding='utf-8') as f:
                        f.write(str(processed) + '\n\n')
                        f.write(str(tree))
                except Exception as err:
                    verbose and logging.warning('\tCan not process the file: %s, Error %s', file, err)
    return processed, tree


def readData(fileName):
    with open(fileName, 'rb') as f:
        bindata = f.read()
        data = pickle.loads(bindata)
        return data

def writeData(data, fileName):
    with open(fileName, 'wb') as f:
        bindata = pickle.dumps(data)
        f.write(bindata)

def createIndex(directory, fileName = '.\\data_index.dat', clear = False, verbose = True):
    if verbose:
        logger= logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.addHandler(logging.FileHandler('processed.log', 'w' if clear else 'a' , 'utf-8'))
    processed, tree = parseDirectory(directory, fileName, clear, verbose)
    with open('./view.txt', 'w', encoding='utf-8') as f:
        f.write(str(processed) + '\n\n')
        f.write(str(tree))

def loadIndex(fileName = '.\\data_index.dat'):
    return readData(fileName)


print('Processing...')
#createIndex(r'./data', './data_index_books.dat', False)
createIndex(r'C:\Users\anton\Documents\Books\[Artigos]', './data_index_articles.dat', True)
print('End...')
