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
