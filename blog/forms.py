from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=4)
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=4)


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='User name', max_length=16, min_length=4, required=True)
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label='First name', required=True)
    last_name = forms.CharField(label='Last name', required=True)
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

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
