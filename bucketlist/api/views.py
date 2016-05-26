from .serializers import (
    UserCreateSerializer,
    # UserLoginSerializer,
    BucketlistSerializer,
    BucketlistItemSerializer,
     )

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from rest_framework import authentication
from django.db.models import Q
from .permissions import IsOwnerOrReadOnly
from app.models import BucketList, BucketListItem
from .pagination import BucketlistLimitOffsetPagination, BucketlistPageNumberPagination
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreateAPIview(CreateAPIView):
    """Handle the URL to  create user."""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class BucketListCreateAPIview(CreateAPIView):
    """Handle the URL to create bucketlists"""

    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BucketListAPIview(ListAPIView):
    """Handle the URL to query bucketlists"""
    serializer_class = BucketlistSerializer
    pagination_class = BucketlistPageNumberPagination
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        queryset_list = BucketList.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(name__icontains=query)
                ).distinct()
        return queryset_list


class BucketListDetailAPIview(RetrieveAPIView):
    """Handle the URL to list all bucketlists"""
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = [IsAuthenticated]


class BucketListUpdateAPIview(UpdateAPIView):
    """Handle the URL to update bucketlists"""
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class BucketListDeleteAPIview(DestroyAPIView):
    """Handle the URL to delete a bucketlists"""
    queryset = BucketList.objects.all()
    serializer_class = BucketlistSerializer
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class BucketlistItemAPIview(CreateAPIView):
    """Handle the URL to create a bucketlist item"""
    serializer_class = BucketlistItemSerializer
    search_fields = ('name', )
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list_id = self.kwargs['pk']
        return BucketListItem.objects.filter(bucketlist=list_id)


class BucketlistDetailItemAPIview(RetrieveAPIView):
    """Handle the URL to list bucketlist items"""
    serializer_class = BucketlistItemSerializer
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list_id = self.kwargs['pk']
        return BucketListItem.objects.filter(bucketlist=list_id)


class BucketlistItemUpdateAPIview(UpdateAPIView):
    """Handle the URL to update bucketlist items"""
    serializer_class = BucketlistItemSerializer
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        list_id = self.kwargs['list_id']
        item_id = self.kwargs['pk']
        bucketlistitem = BucketListItem.objects.filter(
            id=item_id, bucketlist=list_id)
        return bucketlistitem


class BucketlistDeleteItemAPIview(DestroyAPIView):
    """Handle the URL to delete bucketlist items"""
    serializer_class = BucketlistItemSerializer
    authentication_classes = (
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    )
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def delete_queryset(self):
        list_id = self.kwargs['pk']
        return BucketListItem.objects.filter(bucketlist=list_id)
