from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField()
    post = models.ForeignKey('Post')

    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.comment


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = models.TextField()
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
