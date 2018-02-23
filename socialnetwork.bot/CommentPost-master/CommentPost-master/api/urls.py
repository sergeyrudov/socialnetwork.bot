# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^createuser$', views.create_user),
	url(r'^createpost$', views.create_post),
	url(r'^getposts$', views.get_posts),
	url(r'^likeposts$', views.like_post),
    ]