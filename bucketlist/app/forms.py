from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
