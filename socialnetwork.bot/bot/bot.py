from configparser import ConfigParser
import requests
import random
import json


class User:
	def __init__(self):
		self.token = ''
		self.username = self.generator()
		self.password = self.generator()
		self.email = '{0}gmail.com'.format(self.generator())
		self.posts = []
		self.url = 'http://localhost/api/createuser'
		self.create_user()
	
	def generator(self):
		symbols = 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
		result = ''
		for i in range(random.randint(10, 15)):
			result+= random.choice(symbols)
		return result
	
	def create_user(self):
		data = {'username': self.username, 'password': self.password, 'email':self.email}
		response = requests.post(self.url, data=data)
		response = json.loads(response.text)
		self.token = response['token']
	
	def create_post(self):
		self.posts.append(Post(self.token, self.generator(), self.generator()))

class Post:
	def __init__(self, token, name, text):
		self.token = token
		self.name = name
		self.text = text
		self.id = None
		self.url = 'http://localhost/api/createpost'
		self.url_like = 'http://localhost/api/likeposts'
		self.liked = False
		self.create_post()
		
	def create_post(self):
		data = {'token': self.token, 'name': self.name, 'text':self.text}
		response = requests.post(self.url, data=data)
		response = json.loads(response.text)
		self.id = response['id']
		
	def like(self):
		if not self.liked:
			data = {'token':self.token, 'id':self.id}
			requests.post(self.url_like, data)
			self.liked = True
			
			
class Bot:
	def __init__(self):
		self.fileconfig = r'config.ini'
		self.users = []
		self.config = ConfigParser()
		self.config.read_file(open(self.fileconfig))
		self.create_users()
		self.create_posts()
		self.like_posts()
	
	def create_users(self):
		for i in range(int(self.config.get(option='number_of_users', section='Default'))):
			self.users.append(User())
			
	def create_posts(self):
		for i in self.users:
			for j in range(random.randint(1, int(self.config.get(option='max_posts_per_user', section='Default')))):
				i.create_post()
				
	def like_posts(self):
		posts = []
		for i in self.users:
			posts.extend(i.posts)
		for i in range(int(self.config.get(option='max_likes_per_user', section='Default'))):
			p = random.choice(posts)
			p.like()
			posts.remove(p)