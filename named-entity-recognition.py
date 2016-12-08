import nltk
import numpy
rawtext = open('/home/chetan/Documents/sample-certificate.txt','r')
textdata = rawtext.read()
print(textdata)

try:
	tokenized = nltk.word_tokenize(textdata)
	tagged = nltk.pos_tag(tokenized)
	print(tagged)
	namedEnt = nltk.ne_chunk(tagged)
	print(namedEnt)
except Exception as e:
	print(str(e))
		
