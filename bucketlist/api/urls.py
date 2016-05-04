from django.conf.urls import url
from django.contrib import admin

from .views import (BucketListAPIview)

urlpatterns = [
    url(r'^bucketlist/$', BucketListAPIview.as_view()),
]