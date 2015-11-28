"""tsu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'blog.views.home', name='home'),
    url(r'^posts/add/$', 'blog.views.add_post', name='addpost'),
    url(r'^posts/edit/(?P<slug>[-\w]+)/$', 'blog.views.edit_post', name='editpost'),
    url(r'^posts/delete/(?P<slug>[-\w]+)/$', 'blog.views.delete_post', name='deletepost'),
    url(r'^posts/author/(?P<author>[-\w]+)/$', 'blog.views.post_by_author', name='postbyauthor'),
    url(r'^posts/(?P<slug>[-\w]+)/$', 'blog.views.post', name='post'),
    url(r'^categories/create/$', 'blog.views.create_category', name='create_category'),
    url(r'^categories/(?P<slug>[-\w]+)/$', 'blog.views.category', name='category'),
    url(r'^user/register/$', 'blog.views.register', name='register'),
    url(r'^user/login/$', 'blog.views.login', name='login'),
    url(r'^user/logout/$', 'blog.views.logout', name='logout'),
    url(r'^user/profile/$', 'blog.views.profile', name='profile'),
    url(r'^admin/', include(admin.site.urls)),
]
