
import os
import re
import nltk
from nltk import RegexpParser
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from TextExtraction import extractPDF



def extractText(fileName):
	return extractPDF(fileName)


def loadText(fileName):
	f = open(fileName, mode='r', encoding='utf-8')
	return f.read()


def cleaning(text: str):
	text = re.sub(r'\d+', ' ', text)			# remove numbers
	text = re.sub(r'\S*https?:\S*', '', text)   # remove links
	text = re.sub(r'[^\w\s]', ' ', text)		# remove ponctuation
	text = text.lower()							# lower text
	text = re.sub(r'\s+', ' ',   text)			# remove duplicated spaces
	text = text.strip()
	return text


def preprocessingNLP(text):
	#tokens = word_tokenize(text)
	tokens = sent_tokenize(text)
	#stop_words = set(stopwords.words('english'))
	#tokens = [i for i in tokens if not i in stop_words]
	#tokens = [i for i in tokens if len(i) > 2]  # remove math symbols like x
 
	#lemmatizer = WordNetLemmatizer()
	#tokens = list(map(lambda word: lemmatizer.lemmatize(word), tokens))
	return tokens


def extractNouns(tokens):
	tags = nltk.pos_tag(tokens)
	reg_exp = 'Filter: {<NN><NN.?>|<NNS><NN.?>|<NN.?><JJ.?>|<JJ.?>?<NN.?>}'
	rp = nltk.RegexpParser(reg_exp)
	tree = rp.parse(tags)
	#for subtree in tree.subtrees(filter=lambda t: t.node == 'NP'):
		# print the noun phrase as a list of part-of-speech tagged words
	#	print(subtree.leaves())
	#tokens = [chunk for chunk in result if print(chunk) ]
	#tokens = [word for (word, pos) in tokens_tag if pos == 'NN' or pos == 'JJ']
	return tree.leaves()


def run():
	#fileName = os.path.abspath('./data/sample.pdf')
	#text = extractText(fileName)
	fileName = os.path.abspath('./data/sample.txt')
	text = loadText(fileName)
	sentences = sent_tokenize(text)
	sentences = [cleaning(sent) for sent in sentences]
	sentences = [word_tokenize(sent) for sent in sentences if sent]
	sentences = [nltk.pos_tag(tokens) for tokens in sentences]
 
	reg_exp = 'NP: {<NN><NN.?>|<NNS><NN.?>|<NN.?><JJ.?>|<JJ.?>?<NN.?>}'
	rp = nltk.RegexpParser(reg_exp)
	sentences = [rp.parse(tags) for tags in sentences]
	result = []
	for tree in sentences:
		for subtree in tree.subtrees(filter=lambda t: t.label() == 'NP'):
			result.append(' '.join([word for (word, _) in subtree]))
	fd = nltk.FreqDist(result)
	# term frequency
	# 1 gram and bigrams
	fd.plot()
	print(result)

 

def downloadNLTK():
	nltk.download('punkt')
	nltk.download('wordnet')
	nltk.download('omw-1.4')
	nltk.download('averaged_perceptron_tagger')

#downloadNLTK()
run()
