from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from .. import forms


def index(request):
    return render(request, 'header.html')


def signin_view(request):
    form = forms.RegistrationForm()
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS,
                                 'Thanks for signing up !')
            return HttpResponseRedirect('/')
    return render(request, 'signup.html', {'form': form})
