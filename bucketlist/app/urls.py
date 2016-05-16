from django.conf.urls import url, include
from app.views import login_view, logout_view, index_view, BucketlistView, BucketlistItemsView, BucketlistItemStatus, BucketlistDeleteView, BucketlistUpdateView

urlpatterns = [
    url(r'^$', index_view.as_view(), name='index'),
    url(r'^login/$', login_view.as_view()),
    url(r'^logout/$', logout_view.as_view()),
    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$', BucketlistItemsView.as_view(), name="bucket_items"),
    url(r'^bucketlists/(?P<bucketlist>[0-9]+)/items/(?P<pk>[0-9]+)/status/$',
        BucketlistItemStatus.as_view(),
        name="bucketlistitems_status"),
    url(r'^bucketlists/(?P<pk>[0-9]+)/delete/$',
        BucketlistDeleteView.as_view(),
        name="bucketlist_delete"),
    url(r'^bucketlists/(?P<pk>[0-9]+)/edit/$',
        BucketlistUpdateView.as_view(),
        name="bucketlist_edit"),
    # url(r'^bucketlists/(?P<pk>[0-9]+)/$', BucketlistDelete.as_view(), name="bucket_del"),
    url(r'^bucketlists/$', BucketlistView.as_view(), name="bucket_add"),
    # url(r'^bucketlists/(?P<pk>[0-9]+)/$', BucketlistUpdate.as_view(), name="bucket_up"),
    
    url(r'^api/', include('api.urls')),
]
