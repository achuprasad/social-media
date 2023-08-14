from django import forms
from django.contrib.auth.models import User

from social_app.models import UserProfile, CustomUser


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username','email', 'password','first_name','last_name']


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']