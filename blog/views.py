from django.contrib.auth import login as user_login, logout as user_logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, LoginForm


def home(request):
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

    data = {
        'form': form
    }
    return render(request, 'login.html', data)


def logout(request):
    user_logout(request=request)
    return redirect('/')
