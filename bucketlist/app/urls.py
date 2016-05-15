from django.conf.urls import url, include
from app.views import login_view, logout_view, index_view, BucketlistView

urlpatterns = [
    url(r'^$', index_view.as_view(), name='index'),
    url(r'^login/$', login_view.as_view()),
    url(r'^logout/$', logout_view.as_view()),
    url(r'^bucketlists/$', BucketlistView.as_view(), name="bucket_add"),
    url(r'^api/', include('api.urls')),
]
