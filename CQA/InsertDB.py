# insert data into db
import sqlite3
import sys

cx = sqlite3.connect('mycqa.db')
fp = open(sys.argv[1], 'r')
count = 0
for line in fp:
	line = line.strip().split('\t')
	q = line[0]
	q_p = line[1]
	try:
		cx.execute('insert into mycqa_Question (quest_str, quest_desc, answer_path) values (?,?,?)', (q, "no temp desc", q_p))
		count += 1
		if count % 10000 == 0:
			cx.commit()
			print count
	except sqlite3.Error as e:
		print e.args[0]
fp.close()
cx.close()
