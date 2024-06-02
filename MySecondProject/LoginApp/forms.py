from django import forms
from LoginApp.models import  UserInfo   
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())  # Hide password field

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ('facebook_id', 'profile_pic')
