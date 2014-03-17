from django.template import loader, Context
from django.shortcuts import render_to_response
from django.http import HttpResponse
from quest_search import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from GetTopic import *
'''
def index(req):
	return HttpResponse('<h1>Hello MyCQA</h1>')
def index(req):
	t = loader.get_template('index.html')
	c = Context({})
	return HttpResponse(t.render(c)) 
def index(req):
	user = {'name':'Tom','sex':'male','age':'23'}
	return render_to_response('index.html',{'user':user})
'''
def index(req):
	return render_to_response('search_index.html',{})
'''
def search(req):
	if req.POST:
		# conduct search command
		quest_list = search_question(req.POST['squest'])
		curr_num = 1
		page_num = range(curr_num, curr_num+10)
		result = get_quest_detail(quest_list)
		res_num = len(result)
		return render_to_response('search_result.html', {'curr_num':curr_num,'page_num':page_num, 'result':result, 'res_num':res_num})
	else:
		return render_to_response('search_index.html', {})
'''
def search(req):
	if req.POST or req.GET:
		if req.POST:
			quest_list = search_question(req.POST['squest'])
			quest = req.POST['squest']
			page = 1
		else:
			quest = req.GET['query']
			quest_list = search_question(quest)
			try:
				page = int(req.GET['page'])
			except Exception, e:
				page = 1
		if len(quest.strip()) < 2:
			return render_to_response('search_index.html', {})
		result = get_quest_detail(quest_list)
		#print quest
		paginator = Paginator(result, 10)
			
		try:
			r_list = paginator.page(page)
		except PageNotAnInteger:
			r_list = paginator.page(1)
		except EmptyPage:
			r_list = paginator.page(paginator.num_pages)
		if (page+10) < r_list.paginator.num_pages:
			page_list = range(page, page+10)
		else:
			page_list = range(page, r_list.paginator.num_pages+1)
		return render_to_response('search_result.html', {'result':r_list, 'page_list':page_list, 'quest':quest})
	else:
		return render_to_response('search_index.html', {})

def viewQuestion(req):
	if req.GET:
		q_path = req.GET['qpath']
		# get question ,desc, answer_list
		content = readFile('/home/xuzhen/'+q_path)
		content = content.replace('&#xa;', '')
		q = getQuestion(content)
		desc = getDesc(content)
		answer_list = getAnswerList(content)
		ans_sum = getPageTopic(content)
		return render_to_response('question_page.html', {'q':q, 'desc':desc, 'answer_list':answer_list,'ans_sum':ans_sum})
	else:
		print 'No Get!'
		return render_to_response('search_index.html', {})
# Create your views here.
