from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import Post, Post_Category


class LoginForm(forms.Form):
    username = forms.CharField(label='', required=True, min_length=4,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'სახელი',
                               }))
    password = forms.CharField(label='', required=True, min_length=4,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'პაროლი',
                               }))


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='', max_length=16, min_length=4, required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'მომხმარებელი'
                               }))
    email = forms.EmailField(label='', required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'მეილი'
                             }))
    first_name = forms.CharField(label='', required=True,
                                 widget=forms.TextInput(attrs={
                                     'placeholder': 'სახელი'
                                 }))
    last_name = forms.CharField(label='', required=True,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'გვარი'
                                }))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'პაროლი'
    }))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'placeholder': 'დაადასტურეთ პაროლი'
    }))

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            exists = User.objects.get(username=username)
            if exists:
                raise forms.ValidationError("this username already exists.")
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            exists = User.objects.get(email=email)
            if exists:
                raise forms.ValidationError('this email already exists')
        except User.DoesNotExist:
            return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if len(password1) <= 4:
            raise forms.ValidationError('passwords is too short')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('passwords do not match')
        return password2


class CommentForm(forms.Form):
    comment = forms.CharField(label='', min_length=1, max_length=5000, widget=forms.Textarea(attrs={
        'placeholder': 'კომენტარი'
    }))

    def clean_comment(self):
        comment_text = self.cleaned_data['comment']

        if len(comment_text) > 5000:
            raise forms.ValidationError('comment is too long')

        if len(comment_text) == 0:
            raise forms.ValidationError('empty comments are not allowed')

        return comment_text


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user', 'date', 'slug', 'categories']


CategoryFormSet = inlineformset_factory(Post, Post_Category, fields=['category'], extra=1)
