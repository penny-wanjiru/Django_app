from django import forms

from models import UserProfile


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
