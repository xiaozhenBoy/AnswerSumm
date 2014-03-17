# -*- coding: utf-8 -*-
'''
create word graph and random walk on the graph
'''
import math
import nltk
from CanPhraseGeneration import *

def getStopWord():
	stop_dict = {}
	fp = open('/home/xuzhen/dijango/CQA/mycqa/stopword.txt', 'r')
	for line in fp:
		line = line.strip()
		if line not in stop_dict:
			stop_dict[line] = line
	fp.close()
	return stop_dict
class text_graph:
    '''
    '''
    def __init__(self):
        self.word_id_map = {}
        self.adj_matrix = []
        self.word_deg = []
        self.word_score = []
        self.stop_word_dict = getStopWord()
        self.word_pos_sequence = []
        self.st = NltkNlp()##stanfordPos()#OpenNlp() 
    def loadStopWord(self, stopwordfile):
        '''
        '''
        try:
            fin = open('stopword.txt', 'r')
        except Exception, e:
            print e
            return
        #load stop word #print "Loading stop word!"
        for eachline in fin:
            eachline = eachline.strip()
            self.stop_word_dict[eachline] = 1
        fin.close()
        #print "Stop word loaded!"
    def readWordSequence(self, in_stream):
        '''
        read word sequence from file
        file formate: word/pos word/pos ....
        '''
        #convert to word_pos_sequence list #print "Load word sequence....."
        in_stream = in_stream.lower()
        word_list = self.st.posTagger(in_stream+' .')
        #print word_list #print len(word_list)
        for word_pos in word_list:
            if len(word_pos) == 2:
                word_speech = (word_pos[0],word_pos[1])
                if word_pos[0] in self.stop_word_dict:
                    word_speech = (',',',')
                self.word_pos_sequence.append(word_speech)
    def createWordIdMap(self):
        '''
        get candidate phrase by speech of words
        '''
        tags = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS']#
        #
        word_id = 0
        for item in self.word_pos_sequence:
            word = item[0].strip()
            pos = item[1]
            if pos in tags:
                if word not in self.word_id_map:
                    self.word_id_map[word] = word_id
                    word_id += 1
    def getAdjMatrix(self, window_size):
        '''
        default window_size = 2
        '''
        #initialize adj matrix
        word_num = len(self.word_id_map)
        self.word_deg = [0]*word_num
        for i in range(word_num):
            adj_vector = [0]*word_num
            self.adj_matrix.append(adj_vector)
        #print 'adj_matrix size = ', len(self.adj_matrix),len(self.adj_matrix)

        tags = ['NN','NNS','NNP','NNPS','JJ','JJR','JJS'] #,'VBG'
        #
        for i in range(len(self.word_pos_sequence) - window_size + 1):
            word = self.word_pos_sequence[i][0].strip()
            pos = self.word_pos_sequence[i][1]
            if pos not in tags:
                continue
            else:
                curr_id = self.word_id_map[word]
                for k in range(1, window_size):
                    temp_word = self.word_pos_sequence[i+k][0].strip()
                    temp_pos = self.word_pos_sequence[i+k][1]
                    if temp_pos in ['.']:
                        break;
                    if temp_pos in tags:
                        temp_id = self.word_id_map[temp_word]
                        self.adj_matrix[curr_id][temp_id] = 1.0
                        self.adj_matrix[temp_id][curr_id] = 1.0
        for i in range(len(self.word_pos_sequence) - window_size + 1, len(self.word_pos_sequence)):
            word = self.word_pos_sequence[i][0].strip()
            pos = self.word_pos_sequence[i][1]
            if pos not in tags:
                continue
            curr_id = self.word_id_map[word]
            for k in range(i+1, len(self.word_pos_sequence)):
                temp_word = self.word_pos_sequence[k][0].strip()
                temp_pos = self.word_pos_sequence[k][1]
                if temp_pos not in tags:
                    continue
                else:
                    temp_id = self.word_id_map[temp_word]
                    self.adj_matrix[curr_id][temp_id] = 1.0
                    self.adj_matrix[temp_id][curr_id] = 1.0
        #get degree of each word
        #trival the adj_matrix
        for i in range(word_num):
            for j in range(word_num):
                self.word_deg[i] += self.adj_matrix[i][j]
    def getTextRank(self):
        '''
        '''
        word_num = len(self.word_id_map)
        self.word_score = [1.0/word_num]*word_num
        #iterator to text rank
        #computation word score #print 'Start to compute word score ...'
        d = 0.85
        it = 1
        max_it = 1000
        ibsno = word_num * 0.0001
        for it in range(max_it):
            new_word_score = [(1.0-d)/word_num]*word_num
            for i in range(len(self.word_score)):
                for j in range(len(self.word_score)):
                    if self.word_deg[j] != 0.0:
                        new_word_score[i] += d * self.adj_matrix[j][i] * self.word_score[j]/self.word_deg[j]
            addtion = self.computeScoreAddtion(new_word_score)
            self.word_score = new_word_score  #print 'iter = ', it, 'change = ', addtion
            if addtion <= ibsno:
                break
        #print 'Text Rank--Word Score calculated!' #print self.word_score #print self.word_id_map
    def computeScoreAddtion(self, new_word_score):
        '''
        compute the addition above new_page_score
        '''
        addtion = 0
        for i in range(len(self.word_score)):
            addtion += math.fabs(self.word_score[i] - new_word_score[i])
        return addtion
    def getCandidatPhraseEx(self, temp_k):
        candidate_phrase = superGenerateCanPhrase(self.word_pos_sequence)
        phrase_score = {}
        for phrase in candidate_phrase:
            wl = phrase.strip().lower().split(' ')
            score = 0.0
            for word in wl:
                word = word.strip()
                if word in self.word_id_map:
                    score = score + self.word_score[self.word_id_map[word]]
            phrase_score[phrase] = score
        candidate_phrase_list = sorted(phrase_score.items(), key=lambda d: d[1], reverse = True)
        k_len = temp_k
        #print candidate_phrase_list
        key_list = []
        if len(candidate_phrase_list) < k_len:
            k_len = len(candidate_phrase_list)
        for i in range(k_len):
            key_list.append(candidate_phrase_list[i][0])
        return key_list
    def ExtractKeyPhrase(self, instream, k):
        self.word_id_map = {}
        self.adj_matrix = []
        self.word_deg = []
        self.word_score = []
        self.stop_word_dict = {}
        self.word_pos_sequence = []
        self.readWordSequence(instream)
        self.createWordIdMap()
        if len(self.word_id_map) < 1:
            return []
        self.getAdjMatrix(3)
        self.getTextRank()
        return self.getCandidatPhraseEx(k)
