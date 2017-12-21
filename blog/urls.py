# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.views import logout  # 直接导入该视图登出,不用再另外写,且接收next_page参数

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.article, name='article_list'),
    url(r'^(?P<article_id>[\d]+)$', views.article_detail, name='article'),
    url(r'^(?P<article_id>[\d]+)/comment$', views.article_detail_comment, name='article_comment'),
    url(r'^article_set=(?P<article_set>.*)$', views.article, name='article_set'),
    url(r'^article_date=(?P<article_date>[0-9]{4}-[0-9]{2})$', views.article, name='article_date'),
    url(r'^logout/', logout, {'next_page': '/blog'}, name="logout"),
    url(r'^login/', views.blog_login, name="login"),
    url(r'^register/', views.blog_register, name="register"),

]
