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
from .forms import UserLoginForm, SignUpForm, BucketListForm
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
            return redirect("/login/")
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
            return redirect("/bucketlists")
        return render(request, "userform.html", {"form": form, "title": title})


class logout_view(TemplateView):

    def get(self, request):
        logout(request)
        return redirect("/")


class BucketlistView(generic.CreateView, generic.ListView):
    template_name = 'Bucketlists.html'
    success_url = '/bucketlists/'
    model = BucketList
    fields = ['name']

    def form_valid(self, form):
        bucketlist = form.save(commit=False)
        bucketlist.user = self.request.user
        return super(BucketlistView, self).form_valid(form)

    def get_queryset(self):
        return BucketList.objects.filter(user=self.request.user.id)
