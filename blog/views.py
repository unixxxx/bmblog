from django.contrib.auth import login as user_login, logout as user_logout, authenticate
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.text import slugify

from .forms import UserRegisterForm, LoginForm, CommentForm, PostForm, CategoryFormSet, CategoryForm
from .models import Post, Category, Comment


def home(request):
    post_list = Post.objects.active();
    try:
        paginator = Paginator(post_list, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'index.html', {'posts': posts})
    except:
        return render(request, 'index.html')


def profile(request):
    posts = Post.objects.get_by_author(request.user.username)
    data = {
        'posts': posts
    }
    return render(request, 'profile.html', data)


def post(request, slug):
    form = CommentForm(request.POST or None)
    try:
        post_item = Post.objects.get_by_slug(slug)

        if form.is_valid():
            comment = Comment()
            comment.comment = form.cleaned_data['comment']
            comment.post = post_item
            comment.user = request.user
            comment.save()

        data = {
            'post': post_item,
            'form': form,
            'comments': post_item.comment_set.all().order_by('-date')
        }

        return render(request, 'post.html', data)
    except Post.DoesNotExist:
        raise Http404('post does not exist')


def post_by_author(request, author):
    try:
        post_list = Post.objects.get_by_author(author)
        paginator = Paginator(post_list, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'index.html', {'posts': posts})
    except Post.DoesNotExist:
        raise Http404('author does not exist')


def edit_post(request, slug=None):
    post = Post.objects.get_by_slug(slug)
    form = PostForm(request.POST or None, instance=post)
    formset = CategoryFormSet(request.POST or None, instance=post)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        slugified = slugify(instance.title)
        try:
            Post.objects.get_by_slug(slugified)
            slugified = slugified + '-' + slugify(instance.text)[:10]
        except Post.DoesNotExist:
            pass
        instance.slug = slugified
        instance.save()
        if formset.is_valid():
            for f in formset:
                categ = f.save(commit=False)
                try:
                    if f.cleaned_data['DELETE'] and categ.id is not None:
                        categ.delete()
                    elif f.cleaned_data['DELETE'] and categ.id is None:
                        pass
                    else:
                        categ.post = instance
                        categ.save()
                except:
                    pass
        # form.save_m2m()
        return redirect(reverse('profile'))
    data = {
        'form': form,
        'formset': formset
    }

    return render(request, 'add_edit_post.html', data)


def add_post(request):
    form = PostForm(request.POST or None)
    formset = CategoryFormSet(request.POST or None)
    categoryform = CategoryForm(request.POST or None)


    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        slugified = slugify(instance.title)
        try:
            Post.objects.get_by_slug(slugified)
            slugified = slugified + '-' + slugify(instance.text)[:10]
        except Post.DoesNotExist:
            pass
        instance.slug = slugified
        instance.save()
        if formset.is_valid():
            for f in formset:
                categ = f.save(commit=False)
                categ.post = instance
                categ.save()
        return redirect(reverse('profile'))
    data = {
        'form': form,
        'categoryform': categoryform,
        'formset': formset
    }
    return render(request, 'add_edit_post.html', data)


def delete_post(request, slug):
    try:
        post_item = Post.objects.get_by_slug(slug)
        post_item.delete()
    except Post.DoesNotExist:
        raise Http404('post not found')
    return redirect(reverse('profile'))


def create_category(request):
    form = CategoryForm(request.POST)
    print(request.POST)
    print(request.GET)
    if form.is_valid():
        instance = form.save(commit=False)
        slugified = slugify(form.cleaned_data['title'])
        try:
            cat = Category.objects.get_by_slug(slugified)
            slugified = slugified + '-' + slugify(slugified)
        except:
            pass
        instance.slug = slugified
        instance.save()

    return redirect(request.POST['path'])


def category(request, slug):
    try:
        current_category = Category.objects.get_by_slug(slug=slug)
    except Category.DoesNotExist:
        raise Http404('category does not exist')
    post_list = current_category.post_set.active()
    try:
        paginator = Paginator(post_list, 10)
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request, 'index.html', {'posts': posts})
    except:
        return render(request, 'index.html')


def register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        password = form.cleaned_data['password1']
        email = form.cleaned_data['email']

        user = User()
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)

        user.save()
        return redirect(reverse('login'))
    data = {
        'form': form
    }
    return render(request, 'register.html', data)


def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user:
            user_login(request=request, user=user)
            return redirect(reverse('home'))
    data = {
        'form': form
    }
    return render(request, 'login.html', data)


def logout(request):
    user_logout(request=request)
    return redirect(reverse('login'))
