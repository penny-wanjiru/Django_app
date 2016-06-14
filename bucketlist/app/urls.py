from django.conf.urls import url
from app.views import (Login_view,
                       Logout_view, RegisterView, BucketlistView,
                       BucketlistItemsView, BucketlistItemStatus,
                       BucketlistDeleteView, BucketlistUpdateView,
                       BucketlistItemDelete, BucketlistItemUpdate
                       )

urlpatterns = [
    url(r'^$', RegisterView.as_view(), name='index'),
    url(r'^login/$', Login_view.as_view(), name='login'),
    url(r'^logout/$', Logout_view.as_view(), name='logout'),

    url(r'^bucketlists/$', BucketlistView.as_view(), name="bucket_add"),

    url(r'^bucketlists/(?P<pk>[0-9]+)/delete/$',
        BucketlistDeleteView.as_view(),
        name="bucketlist_delete"),

    url(r'^bucketlists/(?P<pk>[0-9]+)/edit/$',
        BucketlistUpdateView.as_view(),
        name="bucketlist_edit"),

    url(r'^bucketlists/(?P<pk>[0-9]+)/items/$',
        BucketlistItemsView.as_view(),
        name="bucketlist_items"),

    url(r'^bucketlists/(?P<bucketlist>[0-9]+)/items/(?P<pk>[0-9]+)/delete/$',
        BucketlistItemDelete.as_view(),
        name="bucketlistitems_delete"),

    url(r'^bucketlists/(?P<bucketlist>[0-9]+)/items/(?P<pk>[0-9]+)/edit/$',
        BucketlistItemUpdate.as_view(),
        name="items_edit"),

    url(r'^bucketlists/(?P<bucketlist>[0-9]+)/items/(?P<pk>[0-9]+)/status/$',
        BucketlistItemStatus.as_view(),
        name="bucketlistitems_status"),

]
