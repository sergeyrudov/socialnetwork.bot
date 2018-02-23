# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
import hashlib
from random import choice

# Create your models here.

class Post(models.Model):
	name = models.CharField('Article', max_length=250)
	text = models.TextField('Full description', max_length=250)
	user = models.ForeignKey(User)

	def count_likes(self):
		return len(self.like_set.all())

	def __str__(self):
		return '{0} - {1}'.format(self.name, self.text)

class Like(models.Model):
	post = models.ForeignKey(Post)
	user = models.ForeignKey(User)


	def __str__(self):
		return '{0} - {1}'.format(self.user.username, self.post.name)

class Token(models.Model):
	token = models.CharField(max_length=20)
	user = models.OneToOneField(User)

	def create_token(self, login, password):
		hash = hashlib.sha512('{0}{1}'.format(login, password).encode('utf-8')).hexdigest()
		token = ''
		for i in range(20):
			token += choice(hash)
		self.token = token