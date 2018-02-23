# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from comments.models import Post

# Create your tests here.

class PostTestCase(TestCase):
	def setUp(self):
		post = Post()
		post.name = 'Test post'
		post.text = 'This text'
		post.save()
	
	def test_created_post(self):
		p = Post.objects.get(name='Test post')
		self.assertEqual(p.text, 'This text')
		
		
	def test_getrequest_signup(self):
		c = Client()
		response = c.get('/signup')
		self.assertEqual(response.status_code, 200)
		
	def test_signup(self):
		c = Client()
		response = c.post('/signup', {'username':'vasya', 'password':'123qwerty', 'email':'123@gmail.com'})
		self.assertRedirects(response, '/signin')
		self.assertEqual(response.status_code, 302)