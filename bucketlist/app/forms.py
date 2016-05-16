from django import forms
from .models import CustomUser, BucketList
from django.contrib.auth import(
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

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if username and password:
            user = CustomUser.objects.get(username=username)
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
    email.help_text = ''
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_two']

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     password2 = self.cleaned_data.get('password2')
    #     if password != password2:
    #         raise forms.ValidationError("Passwords do not match")
    #     return password


class BucketListForm(forms.ModelForm):
    """Form for creation of a bucketlist.
    Extends from bucketlistmodel.
    """

    class Meta:
        model = BucketList
        fields = ['name']


class BucketListItemForm(forms.ModelForm):
    """Form for creation of a bucketlist.
       Extends from bucketlistitem model.
    """

    class Meta:
        model = BucketList
        fields = ['name']            
