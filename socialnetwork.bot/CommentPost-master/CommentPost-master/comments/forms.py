from django.db import models
from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User

class PostForm(ModelForm):
	class Meta:
         model = Post
         fields = ['name', 'text']

class SignupForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email']
		
class SigninForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']
		
class ProfileForm(ModelForm):
	class Meta:
		model = User
		fields = ['username','email']
