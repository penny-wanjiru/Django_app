import json

from django.contrib import auth
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
) 

from django.views.generic.edit import View, CreateView, DeleteView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from .forms import UserLoginForm, SignUpForm, BucketListForm, BucketListItemForm
from .models import BucketList, BucketListItem


class index_view(View):
    def get(self, request):
        form = SignUpForm(None)
        signin = UserLoginForm(None)
        context = {"form": form, "signin": signin}
        return render(request, 'Signup.html', context)

    def post(self, request):
        print request.POST
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            login(request, user)
            return redirect("/bucketlists")
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


class BucketlistDeleteView(TemplateView):

    def get(self, request, **kwargs):
        """Retrieve bucketlist id from request body and delete it."""
        bucketlist = BucketList.objects.filter(
            id=kwargs['pk'], user=self.request.user).first()
        bucketlist.delete()
        messages.success(
            request, 'Bucketlist has been deleted successfully!')
        return redirect('/bucketlists/',
                        context_instance=RequestContext(request))


class BucketlistUpdateView(TemplateView):
    template_name = 'Bucketlists.html'

    @csrf_exempt
    def post(self, request, **kwargs):
        bucketlist = BucketList.objects.filter(
            id=kwargs['pk'], user=self.request.user).first()
        # bucketlist.name = json.loads(request.body)['name']
        bucketlist.name = request.POST.get('name')
        bucketlist.save()
        messages.success(
            request, 'You updated successfully!')
        return HttpResponseRedirect('/bucketlists/')


class BucketlistItemsView(View):
    template_name = 'bucketlistitems.html'

    def get(self, request, *args, **kwargs):
        bucketlist = BucketList.objects.get(pk=kwargs.get('pk'))
        items = BucketListItem.objects.filter(bucketlist=bucketlist)
        return render(request, self.template_name, {'items': items, 'bucketlist': bucketlist})

    def post(self, request, **kwargs):
        form = BucketListItemForm(request.POST or None)
        if form.is_valid():
            item_name = request.POST.get('name')
            new_bucketitem = BucketListItem(
                name=item_name,
                bucketlist=BucketList.objects.get(id=kwargs['pk']))
            new_bucketitem.save()
            messages.success(
                request, 'New Bucketlistitem added successfully!')
            return redirect(
                '/bucketlists/' + kwargs['pk'] + '/items/',
                context_instance=RequestContext(request)
            )
        else:
            messages.error(
                request, 'Error at creation!')
            return redirect(
                '/bucketlists/' + kwargs['pk'] + '/items/',
                context_instance=RequestContext(request)
            )


class BucketlistItemStatus(generic.TemplateView):
    """View logic for marking item as done or not."""

    def get(self, request, **kwargs):
        """Retrieve item id from url passed."""
        bucketlistitem_id = kwargs['pk']
        bucketlistitem = BucketListItem.objects.get(id=bucketlistitem_id)
        bucketlistitem.done = False if bucketlistitem.done else True
        bucketlistitem.save()
        return redirect('/bucketlists/' + kwargs['bucketlist'] + '/items/',
                        context_instance=RequestContext(request))


class BucketlistItemDelete(TemplateView):

    def get(self, request, **kwargs):
        """Retrieve bucketlist id from request body and delete it."""
        bucketlist = kwargs['bucketlist']
        bucketlistitem = BucketListItem.objects.filter(
            id=kwargs['pk'], bucketlist_id=bucketlist).first()
        bucketlistitem.delete()
        messages.success(
            request, 'You have just deleted your item!')
        return redirect('/bucketlists/' + kwargs['bucketlist'] + '/items/',
                        context_instance=RequestContext(request))


class BucketlistItemUpdate(TemplateView):

    @csrf_exempt
    def post(self, request, **kwargs):
        bucketlist = kwargs['bucketlist']
        bucketlistitem = BucketListItem.objects.filter(
            id=kwargs['pk'], bucketlist_id=bucketlist).first()
        bucketlistitem.name = request.POST.get('name')
        bucketlistitem.save()
        messages.success(
            request, 'You have updated successfully!')
        return redirect('/bucketlists/')
