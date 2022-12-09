
import re
import nltk
from nltk import RegexpParser
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize



def extractText(fileName):
    pass


def loadText(fileName):
    f = open(fileName, mode='r', encoding='utf-8')
    return f.read()


def cleaning(text: str):
    text = re.sub(r'\d+', ' ', text)			# remove numbers
    text = re.sub(r'\S*https?:\S*', '', text)  # remove links
    text = re.sub(r'[^\w\s]', ' ', text)		# remove ponctuation
    text = text.lower()							# lower text
    text = re.sub(r'\s+', ' ',   text)			# remove duplicated spaces
    text = text.strip()
    return text


def preprocessingNLP(text):
    tokens = word_tokenize(text)
    #stop_words = set(stopwords.words('english'))
    #tokens = [i for i in tokens if not i in stop_words]
    #tokens = [i for i in tokens if len(i) > 2]  # remove math symbols like x
    lemmatizer = WordNetLemmatizer()
    tokens = list(map(lambda word: lemmatizer.lemmatize(word), tokens))
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
	return tree


def run():
	fileName = './data/sample.txt'
	text = loadText(fileName)
	text = cleaning(text)
	tokens = preprocessingNLP(text)
	nouns = extractNouns(tokens)
	print(nouns)

run()
