from django.conf.urls import url

from views import authentication_view

urlpatterns = [
    url(r'^$', authentication_view.index, name='index'),
    # url(r'^$', authentication_view.IndexView.as_view(), name='index'),
    # url(r'^auth/register', views.create_user)
    url(r'^register$', authentication_view.signin_view, name='register'),
]
