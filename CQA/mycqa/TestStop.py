# -*- coding:utf-8 -*-
import sys

fp = open('stopword.txt', 'r')
stop_dict = {}
for line in fp:
	line = line.strip()
	if line not in stop_dict:
		stop_dict[line] = 1
fp.close()
print len(stop_dict)
