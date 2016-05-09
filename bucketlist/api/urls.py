from django.conf.urls import url
from django.contrib import admin

from .views import (
    BucketListAPIview,
    BucketListDetailAPIview,
    BucketListUpdateAPIview,
    BucketListDeleteAPIview,
    BucketListCreateAPIview,
    BucketlistItemAPIview,
    BucketlistItemUpdateAPIview,
    BucketlistDetailItemAPIview,
    BucketlistDeleteItemAPIview
)

urlpatterns = [
    url(r'^bucketlist/$', BucketListAPIview.as_view()),
    url(r'^bucketlist/create/$', BucketListCreateAPIview.as_view()),
    url(r'^bucketlist/(?P<pk>\d+)/$', BucketListDetailAPIview.as_view()),
    url(r'^bucketlist/(?P<pk>\d+)/delete/$', BucketListDeleteAPIview.as_view()),
    url(r'^bucketlist/(?P<pk>\d+)/edit/$', BucketListUpdateAPIview.as_view()),
    url(r'^bucketlist/(?P<pk>\d+)/items/$', BucketlistItemAPIview.as_view()),
    url(r'^bucketlist/(?P<pk>\d+)/items/(?P<list_id>\d+)/delete/$', BucketlistDeleteItemAPIview.as_view()),
    url(r'^bucketlist/(?P<pk>\d+)/items/(?P<list_id>\d+)$', BucketlistDetailItemAPIview.as_view()),
    url(r'^bucketlist/(?P<pk>\d+)/update/(?P<list_id>\d+)$', BucketlistItemUpdateAPIview.as_view()),
]