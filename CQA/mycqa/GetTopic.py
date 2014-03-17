# -*- coding: utf-8 -*-
import nltk
from TextGraphRank import *
import re
from SentenceSimilarity import SentenceSimilarity
import numpy as np

subject_re = "<subject>(.*?)</subject>"
desc_re = "<content>(.*)</content>"
ans_re = "<answer_item>(.*?)</answer_item>"

tg = text_graph() # for topic phrase extraction
ss = SentenceSimilarity() # for word similarity

def readFile(filepath):
	fp = open(filepath, 'r')
	content = ''
	for line in fp:
		line = line.strip()
		content = content + ' ' + line
	fp.close()
	content = content.replace('&#xa;', '')
	return content

def getKeyWord(con):
	sent_list = nltk.sent_tokenize(con)
	if len(sent_list) < 2:
		key_num = 3
	else:
		key_num = 5
	key_list = tg.ExtractKeyPhrase(con, key_num)
	return key_list
def getPageTopic(content):
	#content = readFile(filepath)
	local_list = []
	# suject 
	match = re.search(subject_re, content)
	if match:
		subject = match.group(1)
	match = re.search(desc_re, content)
	desc = ""
	if match:
		desc = match.group(1)
	subject = subject + ' ' + desc
	q_key = getKeyWord(subject)
	local_list.append(q_key)
	# for each answer
	answer_list = re.findall(ans_re, content)
	for answer in answer_list:
		local_list.append(getKeyWord(answer))
	topic_set = combinationOfLocalTopic(local_list)
	# get abstraction
	abstr_list = extractSent(answer_list, topic_set)
	if len(abstr_list)>10:
		abstr_list = abstr_list[0:10]
	return ' '.join(abstr_list)
	#print "over"
def combinationOfLocalTopic(local_list):
	# simple combination
	all_key = []
	for l in local_list:
		for tkey in l:
			if tkey not in all_key:
				all_key.append(tkey)
	# semantic combination
	sub_topic_num = len(all_key)
	sim_matrix = np.zeros((sub_topic_num, sub_topic_num))
	for i in xrange(sub_topic_num):
		for j in xrange(sub_topic_num):
			sim = ss.getSentSimi(all_key[i], all_key[j])
			sim_matrix[i][j] = sim_matrix[j][i] = sim
	# get global topic set
	visited_list = []
	topic_set = []
	for ind, key in enumerate(all_key):
		if key in visited_list:
			continue
		sim_key = sim_matrix[ind]
		can_list = [] # if sim > 0.5, the two topic may be similarity, so select one as sub_topic is ok
		can_list.append(key)
		for i in range(len(sim_key)):
			if sim_key[i] >= 0.4 and all_key[i] not in visited_list:
				can_list.append(all_key[i])
		sub_can = can_list[0]
		min_len = len(sub_can.split())
		for j in range(1, len(can_list)):
			curr_len = len(can_list[j].split())
			if curr_len < min_len:
				sub_can = can_list[j]
				min_len = curr_len
		topic_set.append(sub_can)
		visited_list.extend(can_list)
	# return global topic
	return topic_set
def extractSent(answer_list, topic_set):
	# extract sentence based on topic set.
	sent_list = []
	for i in xrange(1, len(answer_list)):
		sent_list.extend(nltk.sent_tokenize(answer_list[i]))
	# find sentences that can cover all the topic set
	abstr_list = []
	src_t_num = len(topic_set)
	it = 0
	while (len(topic_set) > 0 and it < src_t_num):
		it += 1
		# calculate sub_topic number of each sentence, add the maxium number sub_topic sentence into abstraction
		sent_tn = getSubTopicNumber(sent_list, topic_set)
		try:
			max_value = max(sent_tn)
		except Exception, e:
			break
		if max_value == 0:
			break
		curr_ind = sent_tn.index(max_value)
		curr_sent = sent_list[curr_ind]
		abstr_list.append(curr_sent)
		sent_list.remove(curr_sent)#del sent_list[curr_ind]
		#print len(sent_list)
		remove_topic = []
		curr_sent = curr_sent.lower()
		for item in topic_set:
			if curr_sent.find(item) != -1:
				remove_topic.append(item)
		for item in remove_topic:
			topic_set.remove(item)
	# end of sentence find
	#print topic_set
	return abstr_list
def getSubTopicNumber(sent_list, topic_set):
	sent_tn = [0]*len(sent_list)
	for ind, sent in enumerate(sent_list):
		sent = sent.lower()
		for st in topic_set:
			if sent.find(st) != -1:
				sent_tn[ind] += 1
	return sent_tn
def getPageTopicOld(filepath, outpath):
	content = readFile(filepath)
	fout = open(outpath, 'w')
	# suject 
	match = re.search(subject_re, content)
	if match:
		subject = match.group(1)
	match = re.search(desc_re, content)
	desc = ""
	if match:
		desc = match.group(1)
	subject = subject + ' ' + desc
	q_key = getKeyWord(subject)
	fout.write(";".join(q_key))
	fout.write('\n')
	fout.flush()
	# for each answer
	answer_list = re.findall(ans_re, content)
	for answer in answer_list:
		ans_key = getKeyWord(answer)
		fout.write(";".join(ans_key)+'\n')
		fout.flush()
	fout.close()
	#print "over"
def getPageTopicEx(filepath, outpath):
	content = readFile(filepath)
	fout = open(outpath, 'w')
	# suject 
	match = re.search(subject_re, content)
	if match:
		subject = match.group(1)
	match = re.search(desc_re, content)
	desc = ""
	if match:
		desc = match.group(1)
	subject = subject + ' ' + desc
	q_key = getKeyWord(subject)
	fout.write(";".join(q_key))
	fout.write('\n')
	fout.flush()
	# for each answer
	answer_list = re.findall(ans_re, content)
	ans_key = getKeyWord(' '.join(answer_list))
	fout.write(";".join(ans_key)+'\n')
	fout.flush()
	fout.close()
	#print "over"
