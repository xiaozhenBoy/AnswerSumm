# not accurate search from db
import sqlite3
import re

sub_re = '<subject>(.*?)</subject>'
ans_re = '<answer_item>(.*?)</answer_item>'
con_re = '<content>(.*?)</content>'
# globle db 
try:
	sqlite_conn = sqlite3.connect('/home/xuzhen/dijango/CQA/mycqa.db',check_same_thread=False)
except sqlite3.Error, e:
	print "Connect sqlite database failed!"
class SearchResultItem():
	q = ''
	q_des = ''
	q_ans = ''
	q_path = ''
def search_question(quest):
	sql_cursor = sqlite_conn.cursor()
	# constructure query
        #search_sent = "select * from tbl_question where quest_str like '%';"
	#sql_cursor.execute('select * from mycqa_Question')
	sql_cursor.execute("select * from mycqa_Question where quest_str like ?", ('%'+quest+'%',))
	quest_list = sql_cursor.fetchall()
	sql_cursor.close()
	return quest_list
def get_quest_detail(quest_list):
	result = []
	for quest in quest_list:
		srt = SearchResultItem()
		srt.q = quest[1]
		srt.q_ans = readFirstAns('/home/xuzhen/' + quest[3])
		srt.q_path = quest[3]
		result.append(srt)
	return result
def readFirstAns(qpath):
	con = readFile(qpath)
	match = re.search(ans_re, con)
	if match:
		ans =  match.group(1)
		if len(ans)>300:
			return ans[0:300] + '......'
		else:
			return ans
	else:
		return ""
def readFile(filepath):
	fp = open(filepath, 'r')
	content = ''
	for line in fp:
		line = line.strip()
		content = content + ' '	+ line
	fp.close()
	return content
def getQuestion(content):
	match = re.search(sub_re, content)
	if match:
		return match.group(1)
	else:
		return ""
def getDesc(content):
	match = re.search(con_re, content)
	if match:
		return match.group(1)
	else:
		return ""
def getAnswerList(content):
	match = re.findall(ans_re, content)
	if match:
		return match
	else:
		return []
