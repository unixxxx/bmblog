from django.contrib import admin

from .models import Comment, Post, Category


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment', 'date']
    list_filter = ['user__username', 'date']
    search_fields = ['comment']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'date']
    list_filter = ['user__username', 'categories', 'active', 'date']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',), }
    inlines = [CommentInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',), }
