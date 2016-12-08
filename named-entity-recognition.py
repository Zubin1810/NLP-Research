import os
import re
from pathlib import Path
from itertools import groupby
import nltk
from nltk.tag import StanfordNERTagger
import PyPDF2

# Stanford NER(Named Entity Recognition) Library Setup.
# Download stanford-ner-2015-12-09.zip
# Set Environment Variables
# export CLASSPATH=/home/chetan/Downloads/install/stanford-ner-2015-12-09/stanford-ner.jar
# export STANFORD_MODELS=/home/chetan/Downloads/install/stanford-ner-2015-12-09/classifiers


if ((not Path('/home/chetan/Documents/sample-certificate.txt').is_file()) or (os.stat('/home/chetan/Documents/sample-certificate.txt').st_size == 0)):
	# read pdf file and create text file
	print('Inside')
	certdata = open('/home/chetan/Documents/certificate.pdf','rb')
	pdfReader = PyPDF2.PdfFileReader(certdata)
	firstPage = pdfReader.getPage(0)
	certText = open('/home/chetan/Documents/sample-certificate.txt','w')
	certText.write(firstPage.extractText().replace('\n','').strip())
	certText.close()
	
with open('/home/chetan/Documents/sample-certificate.txt','r') as file:
	text = file.read()

# Agreement Number regex pattern
agreement_pattern = re.compile(r'BP(\d{8})')
agreement_number = agreement_pattern.search(text)
print('Agreement Number: ' + str(agreement_number.group(0)))

# Agreement Dated regex pattern
agreement_date_pattern = re.compile(r'\d{2}(st?|nd?|rd?|th?)\s+(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{4}')
agreement_date = agreement_date_pattern.search(text)
print('Agreement Dated: ' +str(agreement_date.group(0)))

# Named Entity Recognition : to get BP Name and Consultant Name in Invoice
st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz') 
stanford_ne = st.tag(text.split())

outer_block = []
inner_block = []

for value, tag in st.tag(text.split()):
	if tag != 'O':
		inner_block.append((value, tag))
	else:
		if inner_block:
			outer_block.append(inner_block)
			inner_block = []
if inner_block:
	outer_block.append(inner_block)

named_entities_list = [" ".join([value for value, tag in ne]) for ne in outer_block]
print('BP Name: '+str(named_entities_list[0]))
print('Consultant Name: '+str(named_entities_list[1]))

# Contract Effective Date and Contract End Date Regex Handler
contract_dates = re.findall(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', text)
print('Contract Effective Date: '+ contract_dates[0])
print('Contract End Date: '+ contract_dates[1])
