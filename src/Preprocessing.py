
import os
import re
import nltk
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


def getNgrams(sentences, n):
    reg_exp = 'NP: {<JJ.?>}'
    if n == 2:
        reg_exp = 'NP: {<NN><NN.?>|<NNS><NN.?>|<JJ.?><NN.?>|<NN.?><JJ.?>}'
    elif n == 3:
        reg_exp = 'NP: {<NN><NN.?><NN.?>|<NNS><NN.?><NN.?>|<JJ.?><NN.?><NN.?>|<NN.?><NN.?><JJ.?>}'
    rp = nltk.RegexpParser(reg_exp)
    sentences = [rp.parse(tags) for tags in sentences]
    result = []
    for tree in sentences:
        for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
            result.append(' '.join([word for (word, _) in subtree]))
    return result


def extractWords(fileName, isPDF = True):
    #fileName = os.path.abspath('./data/sample.txt')
    fileName = os.path.abspath(fileName)
    text = ''
    if isPDF:
        text = extractPDF(fileName)
    else:
        f = open(fileName, mode='r', encoding='utf-8')
        text = f.read()
    
    sentences = sent_tokenize(text)
    sentences = [cleaning(sent) for sent in sentences]
    sentences = [word_tokenize(sent) for sent in sentences if sent]
    sentences = [nltk.pos_tag(tokens) for tokens in sentences]

    onegram = getNgrams(sentences, 1)
    bigram = getNgrams(sentences, 2)
    trigram = getNgrams(sentences, 3)
    result = onegram + bigram + trigram

    fd = nltk.FreqDist(result)
    return fd.items(), fd[fd.max()], fd.N()


def downloadNLTK():
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('averaged_perceptron_tagger')
