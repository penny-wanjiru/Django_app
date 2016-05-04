from django.conf.urls import url, include
from app.views import register_view, login_view, logout_view

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^register/$', 'app.views.register_view'),
    url(r'^login/$', 'app.views.login_view'),
    url(r'^logout/$', 'app.views.logout_view'),
    url(r'^api/', include('api.urls')),
]
