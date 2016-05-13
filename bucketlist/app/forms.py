from django.contrib.auth.models import User
from django import forms
from .models import CustomUser
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
)


class SignUpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_two']

    def clean(self):
        print 'cleaned data:'
        print self.cleaned_data
        password = self.cleaned_data['password']
        password_two = self.cleaned_data['password_two']

        if not (password == password_two):
            raise forms.ValidationError("Passwords do not match")
        return self.cleaned_data


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if username and password:
            user = authenticate(username=username, password=password)
            print 'username: %s' % username
            print 'password: %s' % password
            print len(password)
            print 'user'
            print type(user)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is no longer active')
        return self.cleaned_data


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     if password != password2:
    #         raise forms.ValidationError("Passwords do not match")
    #     return password


    
