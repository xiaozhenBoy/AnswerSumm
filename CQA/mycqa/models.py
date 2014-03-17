from django.db import models

class User(models.Model):
	user_id = models.CharField(max_length=50, primary_key=True)
	nick_name = models.CharField(max_length=50)
	user_pwd = models.CharField(max_length=20)
	level = models.IntegerField()
	answer_number = models.IntegerField()
	best_num = models.IntegerField()
	quest_num = models.IntegerField()
	rev_start = models.IntegerField()
	register_time = models.DateTimeField('Register Time!')
	def __unicode__(self):
		return self.user_id
class Question(models.Model):
	quest_str = models.CharField(max_length=300)
	quest_desc = models.CharField(max_length=500)
	answer_path = models.CharField(max_length=50)
	def __unicode__(self):
		return self.quest_str
