# generate candidate key phrase for given paragraph
# there are many method of candidate generation.
import nltk
from nltk.corpus import stopwords
from nltk.tag.stanford import POSTagger
#from jpype import *
import os.path
import re

# set java environment
#jarpath = os.path.join(os.path.abspath('.'), 'opennlp/')
#startJVM("D:/Program Files (x86)/Java/jdk1.7.0_10/jre/bin/client/jvm.dll", "-ea", "-Djava.class.path=%s" % (jarpath+"opennlp-tools-1.5.3.jar;"))
#CandidatePhraseClass = JClass("candidatePhrase.GetCandidatePhrase")
english_stopwords = stopwords.words('english')

class NltkNlp:
	# all nlp processing, use nltk tool
	def __int__(self):
		# no need of static variable
		pass
	def wordToken(self, para):
		sent_list = nltk.sent_tokenize(para)
		token_list = []
		for sent in sent_list: token_list.extend(nltk.word_tokenize(sent))
		return token_list
	def posTagger(self, para):
		token_list = self.wordToken(para)
		return nltk.pos_tag(token_list)
	def generateCanPhrase(self, para):
		#
		pass
'''
class OpenNlp:
	def __init__(self):
		self.paraHandler = CandidatePhraseClass()
	def posTagger(self, para):
		pos_str = self.paraHandler.posParagraph(para)
		# keep consistence with nltk format
		pos_list = []
		for item in pos_str:
			item = item.strip().split('/')
			w_p = (item[0], item[1])
			pos_list.append(w_p)
		return pos_list
	def generateCanPhrase(self, para):
		phrase_list = self.paraHandler.generateCanPhrase(para)
		# remove a|an|the
		for i in range(len(phrase_list)):
			phrase_list[i] = phrase_list[i].strip().lower()
			term_list = phrase_list[i].split(' ')
			if term_list[0] == 'a' or term_list[0] == 'an' or term_list[0] == 'the':
				phrase_list[i] = ' '.join(term_list[1:])
		#phrase_list = [phrase.replace('-', ' ') for phrase in phrase_list if phrase not in english_stopwords]
		# remove repeat phrase
		new_list = []
		for phrase in phrase_list:
			if phrase not in new_list and len(phrase) > 1:
				new_list.append(phrase)
		phrase_list = new_list
		new_list = []
		for phrase in phrase_list:
			p_len = len(phrase)
			flag = False
			for p2 in phrase_list:
				if p_len >= len(p2):
					continue
				else:
					if isSubStr(phrase, p2):
						flag = True
						break
			if not flag: new_list.append(phrase)
		return new_list
class stanfordPos:
	def __init__(self):
		self.pos_tagger = POSTagger("stanford-postagger/models/english-bidirectional-distsim.tagger","stanford-postagger/stanford-postagger.jar")
	def posTagger(self, content):
		content = content.lower()
		sent_list = nltk.sent_tokenize(content)
		word_list = []
		# tagger content
		for sent in sent_list: word_list.extend(nltk.word_tokenize(sent))
		try:
			word_list = self.pos_tagger.tag(" ".join(word_list).split())
		except Exception, e:
			print "stanford Postagger Error!"
			word_list = nltk.pos_tag(word_list)
		return word_list
'''
# generate candidate method based on word pos tuples
def simpleGenerateCanPhrase(word_speech):
	tags = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS'] #
	candidate_phrase_list = []
	candidate_word_list = []
	for item in word_speech:
		word = item[0].strip()
		pos = item[1]
		if pos not in tags:
			if len(candidate_word_list) > 0:
				phrase = candidate_word_list[0]
				for k in range(1,len(candidate_word_list)):
					phrase = phrase + ' ' + candidate_word_list[k]
				phrase = phrase.strip()
				if phrase not in candidate_phrase_list and phrase not in english_stopwords:
					candidate_phrase_list.append(phrase)
				candidate_word_list = []
		else:
			candidate_word_list.append(word)
	return candidate_phrase_list

def generalGenerateCanPhrase(word_speech):
	# By pos pattern, capture candidate phrase
	# Pattern : (adj)*(NN)*
	# Ref: Rada Mihalcea(2004) && Zhiyuan Liu(2010)
	pos_re = "(JJS?R?)*(NNP?S?)+"
	tags = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS'] #
	wp_len = len(word_speech)
	can_list = []
	i = 0 # start
	j = 0 # end pos
	pos_str = ''
	word_str = ''
	while i<wp_len and j<wp_len-1:
		pos_str = pos_str + word_speech[j][1]
		word_str = word_str +' '+ word_speech[j][0]
		if re.match(pos_re, pos_str) and word_speech[j+1][1] not in ['NN','NNS','NNP','NNPS']:
			if len(word_str) > 0:
				word_str = word_str.strip()
				if word_str not in can_list and word_str not in english_stopwords:
					can_list.append(word_str)
			pos_str = ''
			word_str = ''
			i = j
		else:
			if word_speech[j][1] not in tags:
				pos_str = ''
				word_str = ''
				i = j
		j = j+1
	if re.match(pos_re, pos_str) and len(word_str) > 0:
		can_list.append(word_str.strip())
	return can_list

def generalGeneratePhrase(word_speech):
	# By pos pattern, capture candidate phrase
	# Pattern : (adj)*(NN)*
	# Ref: Rada Mihalcea(2004) && Zhiyuan Liu(2010)
	pos_re = "(JJS?R?)*(NNP?S?)+"
	tags = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS'] #
	wp_len = len(word_speech)
	can_list = []
	i = 0 # start
	j = 0 # end pos
	pos_str = ''
	word_str = ''
	while i<wp_len and j<wp_len-1:
		pos_str = pos_str + word_speech[j][1]
		word_str = word_str +' '+ word_speech[j][0]
		if re.match(pos_re, pos_str) and word_speech[j+1][1] not in ['NN','NNS','NNP','NNPS']:
			if len(word_str) > 0:
				word_str = word_str.strip()
				if word_str not in english_stopwords:
					can_list.append(word_str)
			pos_str = ''
			word_str = ''
			i = j
		else:
			if word_speech[j][1] not in tags:
				pos_str = ''
				word_str = ''
				i = j
		j = j+1
	if re.match(pos_re, pos_str) and len(word_str) > 0:
		can_list.append(word_str.strip())
	return can_list
def superGenerateCanPhrase(word_speech):
	# remove sub string from candidate phrase
	phrase_list = generalGenerateCanPhrase(word_speech)
	new_list = []
	for phrase in phrase_list:
		p_len = len(phrase)
		flag = False
		for p2 in phrase_list:
			if p_len >= len(p2):
				continue
			else:
				if isSubStr(phrase, p2):
					flag = True
					break
		if not flag: new_list.append(phrase)
	return new_list
def isSubStr(s1, s2):
	if len(s1) > len(s2):
		s = s1
		s1 = s2
		s2 = s
	s1 = s1.split()
	s2 = s2.split()
	for item in s1:
		if item not in s2:
			return False
	return True
