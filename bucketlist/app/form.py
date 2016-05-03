from django import forms

from models import *


class RegistrationForm(forms.Form):
    """Create registration form with validation on fields.
    Check against existing users within models.
    """
    firstname = forms.RegexField(regex=r'^[0-9a-zA-Z_]*$',
                                 max_length=30,
                                 widget=forms.TextInput(attrs=dict(
                                     required=True,
                                     render_value=False)),
                                 label='first_name')
    lastname = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()

    def save(self):
        """Save the newly created user."""
        new_user = UserProfile.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        return new_user
