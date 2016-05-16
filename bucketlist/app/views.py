from django.contrib import auth
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
) 
from django.views.generic.edit import View, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views import generic
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from .forms import UserLoginForm, SignUpForm, BucketListForm
from .models import BucketList, BucketListItem


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


class BucketlistItemsView(View):
    template_name = 'bucketlistitems.html'

    def get(self, request, *args, **kwargs):
        bucketlist = BucketList.objects.get(pk=kwargs.get('pk'))
        items = BucketListItem.objects.filter(bucketlist=bucketlist)
        return render(request, self.template_name, {'items': items, 'bucketlist': bucketlist})



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


class BucketlistDetailView(DetailView):
    model = BucketListItem

    def get_context_data(self, **kwargs):
        context = super(BucketlistDetailView, self).get_context_data(**kwargs)
        return redirect('/bucketlists/', 
                        context_instance=RequestContext(request))
    

class BucketlistDeleteView(DeleteView):

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(BucketlistDeleteView, self).get_object()
        if not obj.owner == self.request.user:
            raise Http404
        return obj    


class BucketlistDelete(DeleteView):
    template_name = 'Bucketlists.html'
    success_url = reverse_lazy("index")
    model = BucketList
    fields = ['name']



