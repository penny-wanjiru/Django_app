from .serializers import (
    UserCreateSerializer,
    BucketlistSerializer,
    BucketlistItemSerializer,
)
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView
)

from .pagination import BucketlistLimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from app.models import BucketList, BucketListItem
from django.contrib.auth.models import User


class UserCreateAPIview(CreateAPIView):
    """Handle the URL to  create user."""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class BucketListCreateAPIview(CreateAPIView):
    """Handle the URL to create bucketlists"""

    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BucketListAPIview(ListAPIView):
    """Handle the URL to query bucketlists"""
    serializer_class = BucketlistSerializer
    pagination_class = BucketlistLimitOffsetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self, *args, **kwargs):
        queryset_list = BucketList.objects.filter(user=self.request.user)
        return queryset_list


class BucketListDetailAPIview(RetrieveAPIView):
    """Handle the URL to list all bucketlists"""
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = BucketList.objects.filter(user=self.request.user)
        return queryset_list


class BucketListUpdateAPIview(UpdateAPIView):
    """Handle the URL to update bucketlists"""
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class BucketListDeleteAPIview(DestroyAPIView):
    """Handle the URL to delete a bucketlists"""
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    permission_classes = [IsAuthenticated]


class BucketlistItemCreateAPIView(CreateAPIView):
    """Handle the URL to create buckelist items"""
    queryset = BucketListItem.objects.all()
    serializer_class = BucketlistItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        bucket_pk = self.kwargs.get('bucketlist_id')
        related_bucket = BucketList(pk=bucket_pk)
        serializer.save(bucketlist=related_bucket)


class BucketlistItemUpdateDeleteAPIView(UpdateAPIView, DestroyAPIView):
    """Handle the URL to update and delete bucketlist items"""
    permission_classes = [IsAuthenticated]
    serializer_class = BucketlistItemSerializer
    queryset = BucketListItem.objects.all()
