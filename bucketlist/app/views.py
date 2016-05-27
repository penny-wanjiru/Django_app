import json
from django.contrib import auth
from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
    """Handles the signing in of a user
       methods:"GET","POST" 
    """
    def get(self, request):
        form = SignUpForm(None)
        signin = UserLoginForm(None)
        context = {"form": form, "signin": signin}
        return render(request, 'signup.html', context)

    def post(self, request):
        form = SignUpForm(request.POST or None)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            login(request, user)
            return redirect("/bucketlists")
        context = {"form": form}
        return render(request, 'signup.html', context)


class login_view(View):
    """Handles the login of a user
       methods:"POST" 
    """

    def post(self, request):
        signin = UserLoginForm(request.POST or None)
        signup_form = SignUpForm(None)
        if signin.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/bucketlists")
        return render(request, "signup.html", {"signin": signin, "form": signup_form})


class logout_view(TemplateView):
    """Handles logout of a user """

    def get(self, request):
        logout(request)
        return redirect("/")


class BucketlistView(LoginRequiredMixin, generic.CreateView, generic.ListView):
    """View to create and return list of bucketlist"""
    login_url = '/'
    redirect_field_name = 'login'
    template_name = 'bucketlists.html'
    success_url = '/bucketlists/'
    model = BucketList
    fields = ['name']

    def form_valid(self, form):
        bucketlist = form.save(commit=False)
        bucketlist.user = self.request.user
        return super(BucketlistView, self).form_valid(form)

    def get_queryset(self):
        return BucketList.objects.filter(user=self.request.user.id).order_by('-date_updated')


class BucketlistDeleteView(TemplateView):
    """View that handles deleting of a bucketlist"""

    def get(self, request, **kwargs):
        """Retrieve bucketlist id from request body and delete it."""
        bucketlist = BucketList.objects.filter(
            id=kwargs['pk'], user=self.request.user).first()
        bucketlist.delete()
        messages.success(
            request, 'Your bucketlist has been deleted!')
        return redirect('/bucketlists/',
                        context_instance=RequestContext(request))


class BucketlistUpdateView(TemplateView):
    """View that handles updating of a bucketlist"""
    template_name = 'bucketlists.html'

    @csrf_exempt
    def post(self, request, **kwargs):
        bucketlist = BucketList.objects.filter(
            id=kwargs['pk'], user=self.request.user).first()
        # bucketlist.name = json.loads(request.body)['name']
        bucketlist.name = request.POST.get('name')
        bucketlist.save()
        messages.success(
            request, 'Bucketlist updated successfully!')
        return HttpResponseRedirect('/bucketlists/')


class BucketlistItemsView(LoginRequiredMixin, View):
    """View to create and return list of bucketlist items"""
    login_url = '/'
    redirect_field_name = 'login'
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
    """View that handles deleting an item"""

    def get(self, request, **kwargs):
        bucketlist = kwargs['bucketlist']
        bucketlistitem = BucketListItem.objects.filter(
            id=kwargs['pk'], bucketlist_id=bucketlist).first()
        bucketlistitem.delete()
        messages.success(
            request, 'You have just deleted your item!')
        return redirect('/bucketlists/' + kwargs['bucketlist'] + '/items/',
                        context_instance=RequestContext(request))


class BucketlistItemUpdate(TemplateView):
    """View that handles deleting an item"""
    @csrf_exempt
    def post(self, request, **kwargs):
        bucketlist = kwargs['bucketlist']
        bucketlistitem = BucketListItem.objects.filter(
            id=kwargs['pk'], bucketlist_id=bucketlist).first()
        bucketlistitem.name = request.POST.get('name')
        bucketlistitem.save()
        messages.success(
            request, 'You have updated successfully!')
        return redirect('/bucketlists/'+kwargs['bucketlist']+'/items/')

