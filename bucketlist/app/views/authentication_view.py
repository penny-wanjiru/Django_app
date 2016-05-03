from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic import View
from ..forms import UserForm
from ..models import *


class UserFormView(View):
    form_class = UserForm
    template_name = 'new.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save


def index(request):
    return render(request, 'header.html')            












# def signin_view(request):
#     form = forms.RegistrationForm()
#     if request.method == 'POST':
#         form = forms.RegistrationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save()
#             new_user = authenticate(
#                 username=request.POST['username'],
#                 password=request.POST['password'])
#             login(request, new_user)
#             messages.success(
#                 request, "You've been successfully registered!")
#             user.save()
#             messages.add_message(request, messages.SUCCESS,
#                                  'Thanks for signing up !')
#             return HttpResponseRedirect('/')
#     return render(request, 'signup.html', {'form': form})
