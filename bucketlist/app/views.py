from django.contrib import auth
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
) 
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm


class index(TemplateView):
    def get(self, request):
        return render(request, 'header.html')


class login_view(TemplateView):

    def post(self, request):
        title = "login"
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/")
        return render(request, "new.html", {"form": form, "title": title})


class logout_view(TemplateView):

    def get(request):
        logout(request)
        return redirect("/")


class register_view(TemplateView):

    def post(request):
        title = "Register"
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            new_user = authenticate(username=user.username, password=password)
            login(request, new_user)
            return redirect("/")
        context = {
            "form": form,
            "title": title
        }
        return render(request, "new.html", context)
