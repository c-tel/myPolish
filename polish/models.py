from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db import IntegrityError
import random
from random import choice
from string import ascii_letters
from datetime import datetime, timedelta

class SessionManager(models.Manager):
	def autentificate(self,username, password):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			return None
		if user.check_password(password):
			session = Session()
			session.user = user
			session.key = "".join(choice(ascii_letters) for i in range(64))
			session.save()
			return session.key
		return None
	def exit(self, session):
		session.delete()
	

class UsersProgress(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	current_lesson = models.IntegerField()

class Session(models.Model):
	key = models.CharField(unique=True, max_length=64)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	objects = SessionManager()


class Lesson(models.Model):
	num = models.IntegerField(primary_key=True)
	type = models.CharField(max_length=8)
	title = models.CharField(max_length=32, default='Урок')
	img_src = models.CharField(max_length=32, default='/static/lesson1.ico')


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
	title = models.CharField(max_length=32, default='Тест')

	
class WordQuiz(models.Model):
	quest = models.CharField(max_length=16)
	vars = models.CharField(max_length=64)
	correct = models.CharField(max_length=16, default=None)
	related_test = models.ForeignKey(Test, on_delete=models.CASCADE, default=None)

	
class GrammarQuiz(models.Model):
	sentence = models.CharField(max_length=64)
	gaps = models.CharField(max_length=64)
	correct = models.CharField(max_length=16)
	related_test = models.ForeignKey(Test, on_delete=models.CASCADE)
	trans = models.CharField(max_length=64)
	aab = models.CharField(max_length=1)

class WordRecord(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	word = models.ForeignKey(WordQuiz, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now=True)
	class Meta:
		unique_together = ('user', 'word')


class GrammarRecord(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rule = models.ForeignKey(GrammarQuiz, on_delete=models.CASCADE)


def add_user(username, password):
	user = User.objects.create_user(username=username, password=password)
	user.save()
	progress = UsersProgress()
	progress.user = user
	progress.current_lesson = 1
	progress.save()
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
		words = Word.objects.filter(related_lesson=lesson).values()
		dict = []
		for word in words:
			dict.append(word)
		res = {
			'type' : 'dict',
			'dict' : dict,
			'title' : lesson.title,
			'id' : lesson.pk
		}
	else:
		rules = list(GrammarRule.objects.filter(related_lesson=lesson))
		sources = []
		for rule in rules:
			sources.append(rule.src)
		res = {
			'type' : 'grammar',
			'srcs' : sources,
			'title' : lesson.title,
			'id' : lesson.pk
		}
	return res
	

def get_test_stuff(num, user):
	test = Test.objects.get(num=num)
	res = {}
	if test.type == 'grammar':
		quizes = list(GrammarQuiz.objects.filter(related_test=test))
		ex_records = GrammarRecord.objects.filter(user=user)
		for rec in ex_records:
			quizes = quizes.exclude(pk = rec.rule.pk)
		questions = []
		for quiz in quizes:
			gaps = quiz.gaps.split('&')
			gaps.append(quiz.correct)
			random.shuffle(gaps)
			questions.append({
				'sentence' : quiz.sentence,
				'variants' : gaps,
				'correct' : quiz.correct,
				'trans' : quiz.trans,
				'id' : quiz.pk
			})
		res = {
			'tests' : questions,
			'type' : 'grammar',
			'id' : num,
			'title' : test.title,
		}
	if test.type == 'dict':
		quizes = WordQuiz.objects.filter(related_test=test)
		questions = []
		for quiz in quizes:
			vars = quiz.vars.split('&')
			vars.append(quiz.correct)
			random.shuffle(vars)
			questions.append({
				'word' : quiz.quest,
				'variants' : vars,
				'correct' : quiz.correct,
				'id' : quiz.pk
			})
		res = {
			'tests' : questions,
			'type' : 'dict',
			'id' : num,
			'title' : test.title,

		}
	
	return res


def recordWord(id, user):
	try:
		record = WordRecord()
		record.user = user
		record.word = WordQuiz.objects.get(pk=id)
		record.save()
	except IntegrityError:
		pass

def next_lesson(user, id):
	progress = UsersProgress.objects.get(user=user)
	if int(id) == progress.current_lesson:
		progress.current_lesson = progress.current_lesson + 1 
		progress.save()
	
def get_lessons_info(user):
	progress = UsersProgress.objects.get(user=user)
	level = progress.current_lesson
	lessons = Lesson.objects.all()
	lessons_info = []
	for lesson in lessons:
		lessons_info.append({
			'title' : lesson.title,
			'img_src' : lesson.img_src if lesson.num <=level else '/static/locked.png',
			'id' : lesson.num
		
		})
	tests = Test.objects.filter(num__lte = level)
	tests_info = []
	for test in tests:
		tests_info.append({
			'title' : test.title,
			'id' : test.num
		})
	print(tests_info)
	return {'lessons' : lessons_info, 'tests': tests_info , 'level' : level, 'username' : user.username} 
	
def review(user):
	quizes = []
	records = WordRecord.objects.filter(user=user)
	for rec in records:
		quizes.append(WordQuiz.objects.get(pk = rec.word.pk))
	questions = []
	for quiz in quizes:
		vars = quiz.vars.split('&')
		vars.append(quiz.correct)
		random.shuffle(vars)
		questions.append({
			'word' : quiz.quest,
			'variants' : vars,
			'correct' : quiz.correct,
		})
	random.shuffle(questions)
	res = {
		'tests' : questions,
		'title' : 'Brainstorm'
	}
	return res
	
	
def words_for_today(user):
	return WordRecord.objects.filter(user=user, date__gt=datetime.now() - timedelta(days=1)).count()

def drop(user):
	for record in list(WordRecord.objects.filter(user=user)):
		record.delete()
	progress = UsersProgress.objects.get(user=user)
	progress.current_lesson = 1 
	progress.save()
	