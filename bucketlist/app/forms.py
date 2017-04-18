from django import forms
from .models import User, BucketList, BucketListItem
from django.contrib.auth import(
    login,
    logout,
)
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    """Registration form validation for signing up a user"""
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password', 'password_two']:
            self.fields[fieldname].help_text = None
    
    password_two = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password_two = self.cleaned_data.get('password_two')

        if (not password) or (not username) or (not email) or (not password_two):
            raise forms.ValidationError("All fields are required!")

        if not (password == password_two):
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data

    def save(self):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user


class UserLoginForm(forms.ModelForm):
    """Registration form validation for user login"""

    class Meta:
        model = User
        fields = ['username', 'password']

        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if (not password) or (not username):
            raise forms.ValidationError("All fields are required!")
        return self.cleaned_data


class BucketListForm(forms.ModelForm):
    """Form for creation of a bucketlist"""

    class Meta:
        model = BucketList
        fields = ['name']


class BucketListItemForm(forms.ModelForm):
    """Form for creation of a bucketlist item."""

    class Meta:
        model = BucketListItem
        fields = ['name']
