from django.contrib import auth
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
) 
from django.views.generic import View, TemplateView, CreateView, UpdateView, DeleteView
from django.views import generic
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm, SignUpForm
from .models import BucketList


class index_view(View):
    def get(self, request):
        form = SignUpForm(None)
        context = {"form": form}
        return render(request, 'Signup.html', context)

    def post(self, request):
        print request.POST
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("login/")
        context = {"form": form}
        return render(request, 'Signup.html', context)


class login_view(View):

    def get(self, request):
        form = UserLoginForm(None)
        context = {"form": form}
        return render(request, 'userform.html', context)

    def post(self, request):
        title = "login"
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            print 'panda'
            login(request, user)
            return redirect("/")
        return render(request, "userform.html", {"form": form, "title": title})


class logout_view(TemplateView):

    def get(request):
        logout(request)
        return redirect("/")


class register_view(TemplateView):
    template_name = "new.html"

    def post(self, request):
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

class bucketlist_view(generic.ListView):
    template_name = "Bucketlists.html"

    def get_queryset(self):
        return BucketList.objects.all()

class BucketlistCreate(CreateView):  
    model = BucketList
    fields = ['name']   


