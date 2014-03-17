#
from quest_search import *

q = "How can i have"

quest_list = search_question(q)
print len(quest_list)
result = get_quest_detail(quest_list)
result = result[0:10]
for res in result:
	print res.q,res.q_ans

