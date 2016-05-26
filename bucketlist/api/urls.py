from django.conf.urls import url
from django.contrib import admin

from rest_framework_jwt.views import obtain_jwt_token

from .views import (
    UserCreateAPIview,
    # UserLoginAPIview,
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
    url(r'^register/$', UserCreateAPIview.as_view(), name='reg'),
    # url(r'^login/$', UserLoginAPIview.as_view(), name='login'),
    url(r'^bucketlist/$', BucketListAPIview.as_view(), name='bucket_view'),
    url(r'^bucketlist/create/$', BucketListCreateAPIview.as_view(), name='bucket_create'),
    url(r'^bucketlist/(?P<pk>\d+)/$', BucketListDetailAPIview.as_view(), name='bucket_detail'),
    url(r'^bucketlist/(?P<pk>\d+)/delete/$', BucketListDeleteAPIview.as_view(), name='bucket_del'),
    url(r'^bucketlist/(?P<pk>\d+)/edit/$', BucketListUpdateAPIview.as_view(), name='bucket_edit'),
    url(r'^bucketlist/(?P<pk>\d+)/items/$', BucketlistItemAPIview.as_view(), name='bucket_items'),
    url(r'^bucketlist/(?P<pk>\d+)/items/(?P<list_id>\d+)/delete/$', BucketlistDeleteItemAPIview.as_view()
        , name='bucket_itmdel'),
    url(r'^bucketlist/(?P<pk>\d+)/items/(?P<list_id>\d+)$', BucketlistDetailItemAPIview.as_view()
        , name='item_detail'),
    url(r'^bucketlist/(?P<pk>\d+)/update/(?P<list_id>\d+)$', BucketlistItemUpdateAPIview.as_view(), name='item_update'),
    url(r'^auth/login/$', 'rest_framework_jwt.views.obtain_jwt_token', name='login'),
]