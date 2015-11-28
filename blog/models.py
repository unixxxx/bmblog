from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class CategoryManager(models.QuerySet):
    def get_by_slug(self, slug):
        return self.get(slug=slug)


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    objects = CategoryManager.as_manager()

    def get_absolute_url(self):
        return reverse('category', args=[self.slug])

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


class PostManager(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def get_by_slug(self, slug):
        return self.active().get(slug=slug)

    def get_by_author(self, author):
        return self.active().filter(user__username=author)


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = RichTextField()
    slug = models.SlugField(unique=True, db_index=True)
    active = models.BooleanField(default=True)
    allow_comments = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    categories = models.ManyToManyField(Category, through='Post_Category')

    objects = PostManager.as_manager()

    def get_absolute_url(self):
        return reverse('post', args=[self.slug])

    def get_url_by_author(self):
        return reverse('postbyauthor', kwargs={'author': self.user.username})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']


class Post_Category(models.Model):
    post = models.ForeignKey(Post)
    category = models.ForeignKey(Category)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
