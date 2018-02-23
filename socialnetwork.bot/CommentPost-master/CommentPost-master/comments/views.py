# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.db.utils import IntegrityError
from django.contrib import messages
from .models import Token, Like, Post

# Create your views here.

def like(request, id):
	if not request.user.is_authenticated():
		return redirect(reverse('mainpage'))
	post = Post.objects.get(id=id)
	like = post.like_set.filter(user__username=request.user.username)
	if not like:
		l = Like()
		l.user = request.user
		l.post = post
		l.save()
	else:
		like[0].delete()
	return redirect('/posts/{0}'.format(id))

def post_display(request, id):
	post = Post.objects.get(id=id)
	form = PostForm()
	allpost = Post.objects.all()
	context = {'post': post, 'posts': allpost, 'postform': form}
	return render(request, 'comments/TEMPLATE/index.html', context)

def signup(request):
	if request.user.is_authenticated():
		return redirect(reverse('mainpage'))
	if request.method == 'POST':
		data = request.POST
		try:
			u = User.objects.create_user(username=data['username'], password=data['password'], email=data['email'])
			t = Token()
			t.create_token(data['username'], data['password'])
			u.token = t
			t.save()
			return redirect(reverse('signin'))
		except: 
			messages.info(request, 'User is already registered.')
			return redirect(reverse('signup'))
	else:
		form = SignupForm()
		context = {'form':form}
	return render(request, 'comments/TEMPLATE/signup.html', context)
		
		
def signin(request):
	if request.user.is_authenticated():
		return redirect(reverse('mainpage'))
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect(reverse('signin'))
			else:
				return redirect(reverse('profile'))
		else:
			messages.info(request, 'Incorrect login or password')
			return redirect(reverse('signin'))
	if request.method != 'POST':
		form = SigninForm()
		context = {'form':form}
	return render(request, 'comments/TEMPLATE/signin.html', context)
	
	
def profile(request):
	if request.user.is_authenticated():
		context = {}
		return render(request, 'comments/TEMPLATE/profile.html', context)
	else:
		return redirect(reverse('signin'))
		
		
def logoutuser(request):
	logout(request)
	return redirect(reverse('mainpage'))
	
def main_page(request):
	post = Post.objects.all()
	form = PostForm()
	if post:
		objects = post[0]
		context = {'post': objects, 'posts': post, 'postform': form}
		return render(request, 'comments/TEMPLATE/index.html', context)
	else:
		context = {'postform':form}
		return render(request, 'comments/TEMPLATE/index.html', context)
		
def create_post(request):
	if not request.user.is_authenticated():
		return redirect(reverse('mainpage'))
	if request.method == 'POST':
		post = Post()
		post.name = request.POST['name']
		post.text = request.POST['text']
		post.user = request.user
		post.save()
		return redirect(reverse('simple-post', args=[post.id]))
		
	
	
	
	
	
#messages.add_message(request, messages.INFO, 'Hello world.')
#messages.debug(request, '%s SQL statements were executed.' % count)
#messages.info(request, 'Three credits remain in your account.')
#messages.success(request, 'Profile details updated.')
#messages.warning(request, 'Your account expires in three days.')
#messages.error(request, 'Document deleted.')