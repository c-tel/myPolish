from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
import random
from random import choice
from string import ascii_letters


class SessionManager(models.Manager):
	def autentificate(self,username, password):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return None
		if user.check_password(password):
			session = Session()
			session.user = user
			session.key = "".join(random.choice(ascii_letters) for i in range(64))
			session.save()
			return session.key
		return None
	def exit(self, session):
		session.delete();
	
class Session(models.Model):
	key = models.CharField(unique=True, max_length=64)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	objects = SessionManager()

class Lesson(models.Model):
	num = models.IntegerField(primary_key=True)
	type = models.CharField(max_length=8)
	
class Word(models.Model):
	pl = models.CharField(max_length=32)
	uk = models.CharField(max_length=32)
	transcript = models.CharField(max_length=32)
	related_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class GrammarRule(models.Model):
	src = models.CharField(max_length=32)
	related_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

class Test(models.Model):
	num = models.IntegerField(primary_key=True)
	type = models.CharField(max_length=8)

class WordQuiz(models.Model):
	quest = models.CharField(max_length=16)
	vars = models.CharField(max_length=64)
	ans = models.CharField(max_length=16)

def add_user(username, password):
	user = User.objects.create_user(username=username, password=password)
	user.save()
	return user

def not_reserved(username):
	try:
		User.objects.get(username=username)
		return False
	except User.DoesNotExist:
		return True

def get_lesson_stuff(num):
	lesson = Lesson.objects.get(num=num)
	res = {}
	if lesson.type == 'dict':
		words = list(Word.objects.filter(related_lesson=lesson))
		dict = []
		for word in words:
			dict.append([word.pl, word.uk, word.transcript])
		res = {
			'type' : 'dict',
			'dict' : dict
		}
	else:
		rules = list(GrammarRule.objects.filter(related_lesson=lesson))
		sources = []
		for rule in rules:
			sources.append(rule.src)
		res = {
			'type' : 'grammar',
			'srcs' : sources
		}
	return res
		
