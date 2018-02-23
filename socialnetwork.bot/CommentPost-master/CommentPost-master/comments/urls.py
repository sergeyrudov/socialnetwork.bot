# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^([0-9]+)$', views.post_display, name='simple-post'),
	url(r'^([0-9]+)/like$', views.like, name='like-post'),
	url(r'^create$', views.create_post, name='create-post'),
    ]