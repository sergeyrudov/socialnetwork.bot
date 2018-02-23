from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from comments.models import Post, Like, Token
from django.contrib.auth.models import User
from django.http import JsonResponse
# Create your views here.

@csrf_exempt
def create_user(request):
	if request.method == 'POST':
		data = request.POST
		user = User.objects.create_user(username=data['username'], email=data['email'],password=['password'])
		token = Token()
		token.create_token(data['username'], data['password'])
		user.token = token
		token.save()
		response = {'response':'OK', 'token': token.token}
		return JsonResponse(response, safe=False)
@csrf_exempt		
def create_post(request):
	if request.method == 'POST':
		data = request.POST
		user = User.objects.get(token__token=data['token'])
		post = Post()
		post.name = data['name']
		post.text = data['text']
		post.user = user
		post.save()
		response = {'response': 'OK', 'id': post.id}
		return JsonResponse(response, safe=False)

def get_posts(request):
	posts = []
	for i in Post.objects.all():
		posts.append({'name': i.name, 'text': i.text, 'id': i.id})
	response = {'response': 'OK', 'posts': posts}
	return JsonResponse(response, safe=False)

@csrf_exempt	
def like_post(request):
	if request.method == 'POST':
		data = request.POST
		post = Post.objects.get(id=int(data['id']))
		user = User.objects.get(token__token=data['token'])
		like = Like.objects.filter(post=post)
		if not like:
			like = Like()
			like.user = user
			like.post = post
			like.save()
			response = {'response': 'ok'}
			return JsonResponse(response, safe=False)
		response = {'response': 'error'}
		return JsonResponse(response, safe=False)