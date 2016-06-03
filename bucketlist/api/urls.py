from django.conf.urls import url

import rest_framework_jwt.views

from .views import (
    UserCreateAPIview,
    BucketListAPIview,
    BucketListDetailAPIview,
    BucketListUpdateAPIview,
    BucketListDeleteAPIview,
    BucketListCreateAPIview,
    BucketlistItemCreateAPIView,
    BucketlistItemUpdateDeleteAPIView
)

urlpatterns = [
    url(r'^auth/register/$', UserCreateAPIview.as_view(), name='reg'),
    url(r'^auth/login/$', rest_framework_jwt.views.obtain_jwt_token, name='logins'),
    url(r'^bucketlist/$', BucketListAPIview.as_view(), name='bucket_view'),
    url(r'^bucketlist/create/$', BucketListCreateAPIview.as_view(), name='bucket_create'),
    url(r'^bucketlist/(?P<pk>\d+)/$', BucketListDetailAPIview.as_view(), name='bucket_detail'),
    url(r'^bucketlist/(?P<pk>\d+)/delete/$', BucketListDeleteAPIview.as_view(), name='bucket_del'),
    url(r'^bucketlist/(?P<pk>\d+)/edit/$', BucketListUpdateAPIview.as_view(), name='bucket_edit'),
    url(r'^bucketlist/(?P<bucketlist_id>[0-9]+)/items/$',
        BucketlistItemCreateAPIView.as_view()),
    url(r'^bucketlist/(?P<bucketlist_id>[0-9]+)/items/(?P<pk>[0-9]+)$',
        BucketlistItemUpdateDeleteAPIView.as_view()),
    
]