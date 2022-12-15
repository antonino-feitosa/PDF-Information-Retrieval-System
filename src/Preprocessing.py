
import os
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from TextExtraction import extractPDF


def cleaning(text: str):
    text = re.sub(r'\d+', ' ', text)			# remove numbers
    text = re.sub(r'\S*https?:\S*', '', text)   # remove links
    text = re.sub(r'[^\w\s]', ' ', text)		# remove ponctuation
    text = text.lower()							# lower text
    text = re.sub(r'\s+', ' ',   text)			# remove duplicated spaces
    text = text.strip()
    return text


def getNgrams(sentences, n, minSize = 4):
    reg_exp = 'NP: {<NN.?>}'
    if n == 2:
        reg_exp = 'NP: {<NN.?><NN.?>|<JJ.?><NN.?>|<NN.?><JJ.?>|<RB.?><NN.?>|<NN.?><RB.?>}'
    elif n == 3:
        reg_exp = 'NP: {<NN.?><NN.?><NN.?>|<JJ.?><NN.?><NN.?>|<NN.?><NN.?><JJ.?>|<RB.?><NN.?><NN.?>|<NN.?><NN.?><RB.?>}'
    rp = nltk.RegexpParser(reg_exp)
    sentences = [rp.parse(tags) for tags in sentences]
    result = []
    for tree in sentences:
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            word = ' '.join([word for (word, _) in subtree])
            if len(word) >= n * minSize and word.isascii():
                result.append(word)
    return result


def loadText(fileName, isPDF = True):
    fileName = os.path.abspath(fileName)
    text = ''
    if isPDF:
        text = extractPDF(fileName)
    else:
        f = open(fileName, mode='r', encoding='utf-8')
        text = f.read()
    return text


def extractWords(text, minFreq = 10, minSize = 3, verbose = False):
    sentences = sent_tokenize(text)
    verbose and print('Sentences', sentences)
    sentences = [cleaning(sent) for sent in sentences]
    verbose and print('Clean', sentences)
    sentences = [word_tokenize(sent) for sent in sentences if sent]
    verbose and print('Tokens', sentences)
    
    result = []
    lemmatizer = WordNetLemmatizer()
    for sent in sentences:
        result.append([lemmatizer.lemmatize(token) for token in sent])
    verbose and print('Lemmas', sentences)
    
    sentences = [nltk.pos_tag(sent) for sent in result]
    verbose and print('Tags', sentences)

    onegram = getNgrams(sentences, 1, minSize)
    bigram = getNgrams(sentences, 2, minSize)
    trigram = getNgrams(sentences, 3, minSize)
    result = onegram + bigram + trigram
    verbose and print('Result', sentences)
    
    if not result:
        return [], 0, 0

    fd = nltk.FreqDist(result)
    words = [(w,v) for (w,v) in fd.items() if v >= minFreq]
    return words, fd[fd.max()]


def downloadNLTK():
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('averaged_perceptron_tagger')
