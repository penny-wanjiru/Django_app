from django.conf.urls import url
from django.contrib import admin

from .views import (
    UserCreateAPIview,
    UserLoginAPIview
)

urlpatterns = [
    url(r'^register/$', UserCreateAPIview.as_view()),
    url(r'^login/$', UserLoginAPIview.as_view()),
]
