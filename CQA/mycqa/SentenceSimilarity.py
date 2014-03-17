# compute two sentence similarity
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet

class SentenceSimilarity():
	#
	def __init__(self):
		self.wordList_01 = []
		self.wordList_02 = []
		self.simiMatrix = []
	def getSentSimi(self, sent_01, sent_02):
		sent_01 = sent_01.strip().lower() #preprocess
		sent_02 = sent_02.strip().lower()
		self.wordList_01 = nltk.word_tokenize(sent_01) # tokenize sentence
		self.wordList_02 = nltk.word_tokenize(sent_02)
		self.wordList_01 = [w for w in self.wordList_01 if not w in stopwords.words('english')] # remove stopword
		self.wordList_02 = [w for w in self.wordList_02 if not w in stopwords.words('english')]
		if len(self.wordList_01) == 0 or len(self.wordList_02) == 0: return 0.0 # empty set return zero
		# there no demand of Stem, because of wordnet can handle automaticlly
		self.getSimiMatrix()
		# similarity of two set
		return self.computeSetSimi()
	def getSimiMatrix(self):
		m = len(self.wordList_01)
		n = len(self.wordList_02)
		self.simiMatrix = [[0.0]*n for i in range(m)] #initialize simiMatrix m*n Matrix
		semList_01 = []
		semList_02 = []
		for i in range(m):
			try:
				semList_01.append(wordnet.synsets(self.wordList_01[i]))
			except Exception, e:
				semList_01.append(0.0)
		for i in range(n): 
			try:
				semList_02.append(wordnet.synsets(self.wordList_02[i])) # get synsets of word
			except Exception, e:
				semList_02.append(0.0)
		for i in range(m):
			if len(semList_01[i]) == 0: continue
			for j in range(n):
				if len(semList_02[j]) == 0: continue
				l1 = len(semList_01[i])
				l2 = len(semList_02[j])
				for k in range(l1):
					for h in range(l2):
						try:
							sim = semList_01[i][k].path_similarity(semList_02[j][h])
						except Exception,e:
							sim = 0.0
						if sim > self.simiMatrix[i][j]: self.simiMatrix[i][j] = sim
		#print "End of SimiMatrix!"
	def computeSetSimi(self):
		simMax_r = 0.0
		simMax_c = 0.0
		m = len(self.wordList_01)
		n = len(self.wordList_02)
		for i in range(m): simMax_r += max(self.simiMatrix[i])
		for j in range(n): simMax_c += max([self.simiMatrix[k][j] for k in range(m)])
		sim = (simMax_r + simMax_c) / float(m + n)
		return sim